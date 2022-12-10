from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Comics.models import *
from Comics.serializers import *
from django.db.models import Q


@api_view(['GET'])
def getComics(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''
    comics = Comic.objects.filter(
        Q(title__icontains=query) |
        Q(category__icontains=query) |
        Q(author__icontains=query)
    ).order_by('-updated')

    page = request.GET.get('page')
    paginator = Paginator(comics, 20)
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
def getGenres(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''
    genres = Genre.objects.filter(
        Q(name__icontains=query)

    )
    page = request.GET.get('page')
    paginator = Paginator(genres, 100)
    genres_count = genres.count()
    try:
        genres = paginator.page(page)
    except PageNotAnInteger:
        genres = paginator.page(1)
    except EmptyPage:
        genres = paginator.page(paginator.num_pages)
    if page == None:
        page = 1
    page = int(page)
    print('Page:', page)
    serializer = GenreSerializer(genres, many=True)
    return Response({'genres_count': genres_count, 'genres': serializer.data, 'page': page, 'pages': paginator.num_pages, })


@api_view(['GET'])
def getTopComics(request):
    comics = Comic.objects.filter(rating__gte=10.0).order_by('title')
    serializer = ComicSerializer(comics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getComic(request, pk):
    comic = Comic.objects.get(id=pk)
    serializer = ComicSerializer(comic, many=False)
    return Response({'comic': serializer.data})


@api_view(['GET'])
def getChapters(request, pk):
    comic = Comic.objects.get(id=pk)
    chapters = comic.chapter_set.all().order_by('-updated')
    serializer = ComicSerializer(comic, many=False)
    serializer2 = ChapterSerializer(chapters, many=True)
    return Response({'comic': serializer.data, 'chapters': serializer2.data})


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
