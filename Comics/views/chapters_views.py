from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status


from Comics.models import *
from Comics.serializers import *


@api_view(['GET'])
def getChapters(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    chapters = Chapter.objects.filter(
        name__icontains=query).order_by('-updated')

    page = request.query_params.get('page')
    paginator = Paginator(chapters, 20)

    try:
        chapters = paginator.page(page)
    except PageNotAnInteger:
        chapters = paginator.page(1)
    except EmptyPage:
        chapters = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ChapterSerializer(chapters, many=True)
    return Response({'chapters': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopChapters(request):
    chapters = Chapter.objects.filter(rating__gte=8).order_by('-rating')[0:5]
    serializer = ChapterSerializer(chapters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    serializer = ChapterSerializer(chapter, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createChapter(request):

    chapter = Chapter.objects.create(
        name="Sample Name",

    )
    serializer = ChapterSerializer(chapter, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateChapter(request, pk):
    data = request.data
    chapter = Chapter.objects.get(id=pk)

    chapter.name = data['name']
    chapter.participants = data['participants']
    chapter.comics = data['comics']
    chapter.numReviews = data['numReviews']
    chapter.pages = data['pages']
    chapter.save()

    serializer = ChapterSerializer(chapter, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    chapter.delete()
    return Response('Chapter Deleted')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createChapterReview(request, pk):
    user = request.user
    chapter = Chapter.objects.get(id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = chapter.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Chapter already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            chapters=chapter,
            rating=data['rating'],
            text=data['text'],
        )
        chapter.participants.add(user)
        reviews = chapter.review_set.all()
        chapter.numReviews = len(reviews)
        total = 0
        for i in reviews:
            total += i.rating
        chapter.rating = total / len(reviews)
        chapter.save()
        return Response('Review Added')
