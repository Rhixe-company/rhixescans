from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from Comics.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def comic_search(request):
    form = ComicSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if 'q' in request.GET:
        form = ComicSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(genres=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Comic.objects.filter(query)
    context = {'form': form, 'q': q,
               'results': results}
    return render(request, 'loader/search.html', context)

@login_required(login_url='login')
def bookmark_list(request):
    comics = Comic.objects.filter(favourites=request.user)
    return render(request,
                  'loader/favourites.html',
                  {'comics': comics})

@login_required(login_url='login')
def bookmark(request, pk):
    comic = get_object_or_404(Comic, id=pk)
    if comic.favourites.filter(id=request.user.id).exists():
        comic.favourites.remove(request.user)
    else:
        comic.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def index(request):

    genre = request.GET.get('genre')
    if genre == None:
        comics = Comic.objects.all()
    else:
        comics = Comic.objects.filter(Q(genres__name=genre) |
                                      Q(title=genre))
    genres = Genre.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(comics, 21)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)
    context = {'comics': comics, 'genres': genres}
    return render(request, 'loader/index.html', context)


def comics(request):
    genre = request.GET.get('genre')
    if genre == None:
        comics = Comic.objects.all()
    else:
        comics = Comic.objects.filter(Q(genres__name=genre) |
                                      Q(title=genre))
    genres = Genre.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(comics, 21)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)
    context = {'comics': comics, 'genres': genres}
    return render(request, 'loader/comics.html', context)


def comic(request, pk):
    comic = Comic.objects.get(id=pk)
    fav = bool
    if comic.favourites.filter(id=request.user.id).exists():
        fav = True
    genres = comic.genres.all()
    chapters = comic.chapter_set.all()
    context = {'comic': comic, 'genres': genres, 'chapters': chapters, 'fav':fav}
    return render(request, 'loader/comic.html', context)


def chapterview(request, pk):
    chapter = Chapter.objects.get(id=pk)
    pages = chapter.pages.all()
    chapter_reviews = chapter.review_set.all()
    participants = chapter.participants.all()
    chapters = chapter.comics.chapter_set.all()
    page = request.GET.get('page')
    paginator = Paginator(chapters, 10)
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
        chapter.participants.add(request.user)
        reviews = chapter.review_set.all()
        chapter.numReviews = len(reviews)
        chapter.save()
        return redirect('chapter', pk=chapter.id)
    context = {'chapter': chapter, 'pages': pages,
               'chapter_reviews': chapter_reviews, 'participants': participants,'chapters':chapters}
    return render(request, 'loader/chapter.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Little Hack to work around re-building the usermodel
        try:
            user = User.objects.get(email=email)
            user = authenticate(
                request, username=user.username, password=password)
        except:
            messages.error(request, 'User with this email does not exists')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email OR password is incorrect')

    context = {}
    return render(request, 'loader/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account successfuly created!')

            user = authenticate(request, username=user.username,
                                password=request.POST['password1'])

            if user is not None:
                login(request, user)

            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'index'
            return redirect(index)
        else:
            messages.error(request, 'An error has occured with registration')
    context = {'form': form}
    return render(request, 'loader/register.html', context)


@login_required(login_url='login')
def createComic(request):

    form = ComicForm()
    if request.method == 'POST':
        form = ComicForm(request.POST)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.user = request.user
            comic.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'loader/comic_form.html', context)


@login_required(login_url='login')
def updateComic(request, pk):
    Comics = Comic.objects.get(id=pk)
    form = ComicForm(instance=Comics)

    if request.method == 'POST':
        form = ComicForm(request.POST, instance=Comics)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.user = request.user
            comic.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'loader/comic_form.html', context)


@login_required(login_url='login')
def deleteComic(request, pk):
    comic = Comic.objects.get(id=pk)
    if request.method == 'POST':
        comic.delete()
        return redirect('index')
    return render(request, 'loader/delete.html', {'obj': comic})


@login_required(login_url='login')
def createChapter(request):
    form = ChapterForm()
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.user = request.user
            chapter.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'loader/chapter_form.html', context)


@login_required(login_url='login')
def updateChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    form = ChapterForm(instance=chapter)

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.user = request.user
            chapter.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'loader/chapter_form.html', context)


@login_required(login_url='login')
def deleteChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    if request.method == 'POST':
        chapter.delete()
        return redirect('index')
    return render(request, 'loader/delete.html', {'obj': chapter})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    comics = user.comic_set.all()
    comics_count = comics.count()
    comics_review = user.review_set.all()
    genres = Genre.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(comics, 24)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)
    context = {'user': user, 'comics': comics, 'genres': genres,
               'comics_count': comics_count, 'comics_review': comics_review}
    return render(request, 'loader/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'loader/update-user.html', context)


@login_required(login_url='login')
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.user != review.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        review.delete()
        return redirect('chapter', pk=review.chapter.id)
    return render(request, 'loader/delete.html', {'obj': review})
