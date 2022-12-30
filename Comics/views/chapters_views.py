from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Comics.models import *
from Comics.serializers import *


@api_view(['GET'])
def getChapters(request):
    query = request.GET.get('keyword') if request.GET.get(
        'keyword') != None else ''

    chapters = Chapter.objects.filter(
        name__icontains=query).order_by('-updated')[:3000]
    chapters_count = chapters.count()

    serializer = ChapterSerializer(chapters, many=True)
    context = {'chapters_count': chapters_count, 'chapters': serializer.data}
    return Response(context)


@api_view(['GET'])
def getChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    comicId = chapter.comics
    comic = Comic.objects.get(title=comicId)
    serializer = ChapterSerializer(chapter, many=False)
    serializer1 = ComicSerializer(comic, many=False)
    return Response({'chapter': serializer.data, 'comic': serializer1.data})


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
