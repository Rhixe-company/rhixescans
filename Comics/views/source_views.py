from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
import requests
import tldextract
from bs4 import BeautifulSoup

from Comics.models import *
from Comics.serializers import *


@api_view(['GET'])
def getComics(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    comics = Comic.objects.filter(
        title__icontains=query).order_by('-updated')

    page = request.query_params.get('page')
    paginator = Paginator(comics, 20)

    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ComicSerializer(comics, many=True)
    return Response({'comics': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopComics(request):
    comics = Comic.objects.filter(rating__gte=8).order_by('-rating')[0:5]
    serializer = ComicSerializer(comics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getComic(request, pk):
    Comics = Comic.objects.get(id=pk)
    serializer = ComicSerializer(Comics, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createComic(request):
    user = request.user
    comic = Comic.objects.create(
        user=user,
        title=request.get('title'),
        description=request.get('description'),
        image=request.get('image'),
        rating=request.get('rating'),
        status=request.get('status'),
    )
    serializer = ComicSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetchComics(request):
    Comics = Comic.objects.all()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    baseurl = 'https://asura.gg/manga'
    url_dictionary = {}
    comiclinks = []
    with requests.Session() as s:
        def request(x):
            url = f'{baseurl}/?page={x}'
            r = s.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            return soup.find_all('div', class_='bsx')

        def parse(articles):
            for item in articles:
                for link in item.find_all('a', href=True):
                    comiclinks.append(link['href'])
            for link in comiclinks:
                r = s.get(link, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                chapters = soup.find_all("div", class_='chbox')
                try:
                    title = soup.find(
                        "h1", class_="entry-title").text.strip()
                    new_title = title
                except:
                    print('title not found')
                    pass
                try:
                    rating = soup.find("div", class_="num").text.strip()
                    new_rating = rating
                except:
                    print('rating not found')
                    pass
                try:
                    status = soup.find('div', class_='imptdt').find(
                        'i').text.strip()
                    new_status = status
                except:
                    print('status not found')
                    pass
                try:
                    category = soup.find("div", class_='tsinfo').find(
                        "a").text.strip()
                    new_category = category
                except:
                    print('category not found')
                    pass
                try:
                    image = soup.find(
                        "div", class_="thumb").find('img')['src']
                    new_image = image
                except:
                    print('image not found')
                    pass
                try:
                    description = soup.find(
                        "div", class_='entry-content entry-content-single').find("p").text.strip()
                    new_description = description
                except:
                    print('description not found')
                    pass
                try:
                    genres = soup.find("span", class_="mgen").text.strip()
                    new_genres = genres
                except:
                    print('genres not found')
                    pass
                comic, created = Comic.objects.get_or_create(
                    title=new_title,
                    rating=new_rating,
                    description=new_description,
                    image_url=new_image,
                    status=new_status,

                )
                tag, created = Tag.objects.get_or_create(
                    name=new_category, comics=comic)
                genre, created = Genre.objects.get_or_create(
                    name=new_genres, comics=comic)
                print(f'Saving Comic: {new_title}')
                for page in chapters:
                    chapterlist = []
                    for link in page.find_all('a', href=True):
                        chapterlist.append(link['href'])
                        for link in chapterlist:
                            domain_name = tldextract.extract(
                                link).registered_domain
                            r = s.get(link, headers=headers)
                            if r.status_code == 200:
                                url_dictionary[link] = []
                                soup = BeautifulSoup(
                                    r.content, 'html.parser')

                                try:
                                    name = soup.find(
                                        "h1", class_="entry-title").text.strip()
                                    new_name = name
                                except:
                                    print('name not found')
                                    pass

                                try:
                                    images = soup.find(
                                        'div', class_='rdminimal').find_all('img')
                                except:
                                    print('no images')
                                    pass
                                chapter, created = Chapter.objects.get_or_create(
                                    comics=comic,
                                    name=new_name,
                                )
                                url_dictionary[link].extend(images)
                                cleaned_dictionary = {
                                    key: value for key, value in url_dictionary.items() if len(value) > 0}

                                for key, images in cleaned_dictionary.items():
                                    all_images = []
                                    domain_name = tldextract.extract(
                                        key).registered_domain
                                    for image in images:
                                        source_image_url = image.attrs['src']
                                        if source_image_url.startswith("//"):
                                            pass
                                        elif domain_name not in source_image_url and 'http' not in source_image_url:
                                            url = 'https://' + domain_name + source_image_url
                                            all_images.append(url)
                                        else:
                                            all_images.append(
                                                source_image_url)
                                    new_files = all_images
                                    image, created = Image.objects.get_or_create(
                                        images_url=new_files,
                                        chapters=chapter,
                                    )
                                else:
                                    print('failed')
        x = 1
        while True:
            print(f'Page {x}')
            articles = request(x)
            x = x+1

            if len(articles) != 0:
                parse(articles)
            else:
                break
    serializer = ComicSerializer(Comics, many=True)
    return Response(serializer.data, f'Total Comics = len({articles})')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateComic(request, pk):
    data = request.data
    comic = Comic.objects.get(id=pk)

    comic.title = data['title']
    comic.genres = data['genres']
    comic.image = data['image']
    comic.rating = data['rating']
    comic.status = data['status']
    comic.category = data['category']
    comic.description = data['description']

    comic.save()

    serializer = ComicSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteComic(request, pk):
    comics = Comic.objects.get(id=pk)
    comics.delete()
    return Response('Comic Deleted')


@api_view(['POST'])
def uploadFile(request):
    data = request.data

    comicid = data['comicid']
    comic = comic.objects.get(id=comicid)

    comic.image = request.IMAGES.get('image')
    comic.save()

    return Response('Comic was uploaded')
