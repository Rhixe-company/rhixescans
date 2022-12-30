from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Comics.models import *
from Comics.serializers import *
from django.db.models import Q
from bs4 import BeautifulSoup
from requests_html import HTMLSession


@api_view(['POST'])
@permission_classes([IsAdminUser])
def crawl(request):
    s = HTMLSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"}

    def request(x):
        url = f'https://www.asurascans.com/manga/?page={x}'
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, features='lxml')
        content = soup.find_all('div', class_='bsx')
        return content

    def parse(articles):
        for item in articles:
            for link in item.find_all('a', href=True):
                links = link['href']
                r = s.get(links, headers=headers)
                soup = BeautifulSoup(r.content, features='lxml')
                title = soup.find("h1", class_="entry-title").text.strip()
                rating = float(soup.find("div", class_="num").text.strip())
                category = soup.find(
                    "div", class_='tsinfo').find("a").text.strip()
                image = soup.find("div", class_="thumb").find('img')['src']
                description = soup.find(
                    "div", class_='entry-content entry-content-single').find("p").text.strip()
                status = soup.find('div', class_='imptdt').find(
                    'i').text.strip()
                author = soup.find('span', class_='author').find(
                    'i').text.strip()
                released = soup.select('div.fmed')[0].find(
                    'span').text.strip()
                artist = soup.select('div.fmed')[1].find(
                    'span').text.strip()
                serialized = soup.select('div.fmed')[2].find(
                    'span').text.strip()
                created = soup.select('div.fmed')[4].find(
                    'time').text.strip()
                updated = soup.select('div.fmed')[5].find(
                    'time').text.strip()
                obj, created = ComicsManager.objects.filter(
                    Q(title__icontains=title)
                ).get_or_create(image_url=image, rating=rating, status=status, description=description,  author=author,  artist=artist, category=category, serialized=serialized, released=released, created=created, updated=updated, defaults={'title': title})
                print(f'{title} added')
                g = soup.select("span.mgen a")
                for genre in g:
                    genres = genre.text.strip()
                    obj1, created = Genre.objects.filter(
                        Q(name=genres)
                    ).get_or_create(
                        name=genres, defaults={'name': genres})
                    print(f'{genres} added')
                    obj.genres.add(obj1)
                    obj.save()

                chapters = soup.find_all("div", class_='chbox')
                for chapter in chapters:
                    for l in chapter.find_all('a', href=True):
                        page = l['href']
                        r = s.get(page, headers=headers)
                        soup = BeautifulSoup(r.content, features='lxml')
                        name = soup.find(
                            "h1", class_="entry-title").text.strip()
                        obj2, created = obj.chapter_set.filter(
                            Q(name=name)
                        ).get_or_create(comics=obj, name=name, defaults={'name': name})
                        print(f'{name} added')
                        posts = soup.select(
                            "div.rdminimal img")
                        for p in posts:
                            pages = p['src']
                            obj3, created = obj2.page_set.filter(
                                Q(images_url__icontains=pages)
                            ).get_or_create(images_url=pages, chapters=obj2, defaults={'images_url': pages, 'chapters': obj2})
                            obj2.pages.add(obj3)
                            obj2.numPages = obj2.page_set.all().count()
                            obj2.save()
                            obj.numChapters = obj.chapter_set.all().count()
                            obj.save()

    x = 1
    while True:
        print(f'Page {x}')
        articles = request(x)
        x = x+1

        if len(articles) != 0:
            webtoons = parse(articles)
            print(webtoons)
        else:
            break
    comics = Comic.objects.all()
    serializer = ComicSerializer(comics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getComics(request):
    query = request.GET.get('keyword')

    if query == None:
        comics = Comic.objects.filter(Q(status='Ongoing') |
                                      Q(status='Completed') |
                                      Q(status='Coming Soon')).distinct()
    else:
        comics = Comic.objects.filter(
            Q(title__contains=query) |
            Q(genres__name__contains=query)
        ).distinct()

    page = request.GET.get('page')
    paginator = Paginator(comics, 24)
    comics_count = comics.count()
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

    context = {'comics_count': comics_count, 'comics': serializer.data,
               'page': page, 'pages': paginator.num_pages, }
    return Response(context)


@api_view(['GET'])
@permission_classes([AllowAny])
def getGenres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getTopComics(request):
    comics = Comic.objects.filter(rating__gte=10.0).order_by('title')
    serializer = ComicSerializer(comics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getComic(request, pk):
    comic = Comic.objects.get(id=pk)
    chapters = comic.chapter_set.all()
    serializer = ComicSerializer(comic, many=False)
    serializer1 = ChapterSerializer(chapters, many=True)
    return Response({'comic': serializer.data, 'chapters': serializer1.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createComic(request):
    comic = Comic.objects.create(
        user=request.user,
        title='Sample Name',
        description='Sample Name',
        rating=0.0,
    )

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
@permission_classes([IsAuthenticated])
def uploadImage(request):
    data = request.data

    comicId = data['comiId']
    comic = Comic.objects.get(id=comicId)

    comic.image = request.FILES.get('image')
    comic.save()

    return Response('Image was uploaded')
