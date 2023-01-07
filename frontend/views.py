from django.shortcuts import render
from .forms import *
from Comics.models import *
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    comics = Comic.newmanager.all().order_by('updated')
    page = request.GET.get('page')
    paginator = Paginator(comics, 21)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)
    context = {'comics': comics}
    return render(request, 'frontend/home.html', context)

def comic(request, pk):
    comic = Comic.objects.get(id=pk)
    fav = bool
    if comic.favourites.filter(id=request.user.id).exists():
        fav = True
    genres = comic.genres.all()
    chapters = comic.chapter_set.all()
    context = {'comic': comic, 'genres': genres,
               'chapters': chapters, 'fav': fav}
    return render(request, 'frontend/comic_view.html', context)


@login_required()
def chapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    pages = chapter.pages.all()
    chapter_reviews = chapter.comments.all()
    reviews_count = chapter_reviews.count()
    chapters = chapter.comic.chapter_set.all()
    page = request.GET.get('page')
    paginator = Paginator(chapters, 30)
    try:
        chapters = paginator.page(page)
    except PageNotAnInteger:
        chapters = paginator.page(1)
    except EmptyPage:
        chapters = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        review = Review.objects.create(
            user=request.user,
            chapter=chapter,
            text=request.POST.get('text')
        )
        reviews = chapter.comments.all()
        chapter.numReviews = len(reviews)
        chapter.user = request.user
        chapter.save()
        return redirect('chapter', pk=chapter.id)

    context = {'chapter': chapter, 'pages': pages,
               'chapter_reviews': chapter_reviews,  'chapters': chapters, 'total_reviews': reviews_count}
    return render(request ,'frontend/chapter_view.html', context)


@login_required()
def createComic(request):
    form = ComicForm()
    if request.method == 'POST':
        form = ComicForm(request.POST)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.user = request.user
            comic.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    context = {'form': form}
    return render(request, 'frontend/comic_form.html', context)


@login_required()
def updateComic(request, pk):
    Comics = Comic.objects.get(id=pk)
    form = ComicForm(instance=Comics)

    if request.method == 'POST':
        form = ComicForm(request.POST, instance=Comics)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.user = request.user
            comic.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    context = {'form': form}
    return render(request, 'frontend/comic_form.html', context)


@login_required()
def deleteComic(request, pk):
    comic = Comic.objects.get(id=pk)
    if request.method == 'POST':
        comic.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'frontend/delete.html', {'obj': comic})


@login_required()
def createChapter(request):
    form = ChapterForm()
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.user = request.user
            chapter.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    context = {'form': form}
    return render(request, 'frontend/chapter_form.html', context)


@login_required()
def updateChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    form = ChapterForm(instance=chapter)

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.user = request.user
            chapter.save()
            return redirect('comic', pk=chapter.comic.id)
    context = {'form': form}
    return render(request, 'frontend/chapter_form.html', context)


@login_required()
def deleteChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    if request.method == 'POST':
        chapter.delete()
        return redirect('comic', pk=chapter.comic.id)
    return render(request, 'frontend/delete.html', {'obj': chapter})


@login_required()
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.user != review.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        review.delete()
        return redirect('chapter', pk=review.chapter.id)
    return render(request, 'frontend/delete.html', {'obj': review})
