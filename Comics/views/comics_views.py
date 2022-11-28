from bs4 import BeautifulSoup
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Comics.models import *
from Comics.serializers import *
import requests
from django.db.models import Q


@api_view(['POST'])
@permission_classes([AllowAny])
def scrapeComics(request):
    with requests.Session() as s:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
        baseurl = 'https://asura.gg/manga'
        website, created = Website.objects.get_or_create(
            url=baseurl
        )

        def load(x):
            url = f'{baseurl}/?page={x}'
            r = s.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup.find_all('div', class_='bsx')

        def parse(articles):
            comiclinks = []
            for item in articles:
                for link in item.find_all('a', href=True):
                    comiclinks.append(link['href'])
            for link in comiclinks:
                r = s.get(link, headers=headers)
                print(f'Comics:{link} Status: {r.status_code}')
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    chapters = soup.find_all("div", class_='chbox')
                    try:
                        title = soup.find(
                            "h1", class_="entry-title").text.strip()
                        alreadyExists = Comic.objects.get(
                            title=title)
                    except:
                        print('title not found')
                    try:
                        rating = soup.find(
                            "div", class_="num").text.strip()
                    except:
                        print('rating not found')
                    try:
                        status = soup.find('div', class_='imptdt').find(
                            'i').text.strip()
                    except:
                        print('status not found')
                    try:
                        category = soup.find("div", class_='tsinfo').find(
                            "a").text.strip()
                    except:
                        print('category not found')
                    try:
                        image = soup.find(
                            "div", class_="thumb").find('img')['src']
                    except:
                        print('image not found')
                    try:
                        description = soup.find(
                            "div", class_='entry-content entry-content-single').find("p").text.strip()
                    except:
                        print('description not found')

                    try:
                        genree = soup.find("span", class_="mgen")
                        for objj in genree.find_all('a'):
                            genres = objj.text.strip()
                    except:
                        print('genres not found')
                    try:
                        author = soup.find("div", class_="flex-wrap").find_all(
                            'div', {'class': 'fmed'})[1].find('span').text.strip()
                    except:
                        print('author not found')
                    for page in chapters:
                        chapterlist = []
                        for link in page.find_all('a', href=True):
                            chapterlist.append(link['href'])
                            for link in chapterlist:
                                r = s.get(link, headers=headers)
                                print(
                                    f'Chapter:{link} Status: {r.status_code}')
                                if r.status_code == 200:
                                    soup = BeautifulSoup(
                                        r.text, 'html.parser')
                                    posts = soup.find_all(
                                        "div", class_='rdminimal')
                                    try:
                                        name = soup.find(
                                            "h1", class_="entry-title").text.strip()
                                    except:
                                        print('name not found')
                                        pass

                                    for post in posts:
                                        for page in post.find_all("img", src=True):
                                            pages = page['src']

                                            if alreadyExists:
                                                genre, created = alreadyExists.genres.update_or_create(
                                                    name=genres)

                                                chapter, created = Chapter.objects.get_or_create(
                                                    comics=alreadyExists,
                                                    website=website,
                                                    name=name,
                                                    user=request.user,
                                                )
                                                new_page, created = chapter.pages.get_or_create(
                                                    images_url=pages,
                                                    chapters=chapter
                                                )
                                            else:
                                                comic, created = Comic.objects.get_or_create(
                                                    title=title,
                                                    rating=rating,
                                                    description=description,
                                                    image_url=image,
                                                    status=status,
                                                    category=category,
                                                    author=author,
                                                    website=website,
                                                    user=request.user,
                                                )
                                                genre, created = comic.genres.update_or_create(
                                                    name=genres)
                                                chapter, created = Chapter.objects.get_or_create(
                                                    comics=comic,
                                                    website=website,
                                                    name=name,
                                                    user=request.user,
                                                )
                                                new_page, created = chapter.pages.get_or_create(
                                                    images_url=pages,
                                                    chapters=chapter
                                                )
                                            pass
                                else:
                                    print('failed')
                                    pass
        x = 1

        while True:
            print(f'Page {x}')
            articles = load(x)
            x = x+1

            if len(articles) != 0:
                parse(articles)
            else:
                break
    return Response(f'Completed, total Comics: {len(articles)}')


@api_view(['GET'])
def getComics(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    comics = Comic.objects.filter(
        Q(title__icontains=query) |
        Q(category__icontains=query) |
        Q(author__icontains=query) |
        Q(genres__name__icontains=query)
    ).order_by('updated')
    comics_count = comics.count()
    page = request.query_params.get('page')
    paginator = Paginator(comics, 24)

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

    context = {'comics': serializer.data,
               'page': page, 'pages': paginator.num_pages, 'comics_count': comics_count, }
    return Response(context)


@api_view(['GET'])
def getTopComics(request):
    comics = Comic.objects.filter(rating__gte=9.1).order_by('-rating')[0:10]
    serializer = ComicSerializer(comics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getComic(request, pk):
    comic = Comic.objects.get(id=pk)
    serializer = ComicSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getChapters(request, pk):
    comics = Comic.objects.get(id=pk)
    chapters = comics.chapter_set.all()
    serializer = ChapterSerializer(chapters, many=True)
    return Response({'chapters': serializer.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createComic(request):
    comic = Comic.objects.create(
        user=request.user,
        title=request.POST.get('title'),
        description=request.POST.get('description'),
        image_url=request.POST.get('image_url'),
        rating=request.POST.get('rating'),
        author=request.POST.get('author'),
        status=request.POST.get('status'),
    )
    comic.genres.add(request.POST.get('genres'))
    serializer = ComicSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateComic(request, pk):
    data = request.data
    comic = Comic.objects.get(id=pk)
    comic.user = request.user
    comic.title = data['title']
    comic.image_url = data['image_url']
    comic.rating = data['rating']
    comic.status = data['status']
    comic.description = data['description']
    comic.category = data['category']
    comic.author = data['author']
    comic.save()
    # comic.genres.add(data['genres'])

    serializer = ComicSerializer(comic, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteComic(request, pk):
    comic = Comic.objects.get(id=pk)
    comic.delete()
    return Response('comic Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    comicId = data['comiId']
    comic = Comic.objects.get(id=comicId)

    comic.image = request.FILES.get('image')
    comic.save()

    return Response('Image was uploaded')
