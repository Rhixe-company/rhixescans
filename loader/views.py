from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from Comics.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.views.generic import ListView
# Create your views here.


class CatListView(ListView):
    template_name = 'loader/genre.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['genre'],
            'posts': Comic.objects.filter(genres__name=self.kwargs['genre'])
        }
        return content


def genres_list(request):
    genres_list = Genre.objects.all()
    context = {
        'genres_list': genres_list
    }
    return context


@login_required()
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        comic = get_object_or_404(Comic, id=id)
        if comic.likes.filter(id=request.user.id).exists():
            comic.likes.remove(request.user)
            comic.like_count -= 1
            result = comic.like_count
            comic.save()
        else:
            comic.likes.add(request.user)
            comic.like_count += 1
            result = comic.like_count
            comic.save()

        return JsonResponse({'result': result, })


def comic_search(request):
    form = ComicSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Comic.objects.filter(
                title__contains=search_string)
            data = serializers.serialize(
                'json', list(search_string), fields=('id', 'title', 'image', 'status', 'category'))
            return JsonResponse({'search_string': data})

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


@login_required()
def bookmark_list(request):
    comics = Comic.objects.filter(favourites=request.user)
    return render(request,
                  'loader/favourites.html',
                  {'comics': comics})


@login_required()
def bookmark(request, pk):
    comic = get_object_or_404(Comic, id=pk)
    if comic.favourites.filter(id=request.user.id).exists():
        comic.favourites.remove(request.user)
    else:
        comic.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    comics = Comic.newmanager.filter(Q(title__icontains=q) |
                                     Q(alternativetitle__icontains=q)
                                     )
    page = request.GET.get('page')
    paginator = Paginator(comics, 21)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)
    context = {'comics': comics}
    return render(request, 'loader/index.html', context)


def comics(request):
    comics = Comic.objects.all().order_by('title')
    page = request.GET.get('page')
    paginator = Paginator(comics, 21)
    try:
        comics = paginator.page(page)
    except PageNotAnInteger:
        comics = paginator.page(1)
    except EmptyPage:
        comics = paginator.page(paginator.num_pages)
    context = {'comics': comics}
    return render(request, 'loader/comics.html', context)


def comic(request, pk):
    comic = Comic.objects.get(id=pk)
    fav = bool
    if comic.favourites.filter(id=request.user.id).exists():
        fav = True
    genres = comic.genres.all()
    chapters = comic.chapter_set.all()
    context = {'comic': comic, 'genres': genres,
               'chapters': chapters, 'fav': fav}
    return render(request, 'loader/comic.html', context)


@login_required()
def chapterview(request, pk):
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
        return redirect('loader:chapter', pk=chapter.id)

    context = {'chapter': chapter, 'pages': pages,
               'chapter_reviews': chapter_reviews,  'chapters': chapters, 'total_reviews': reviews_count}
    return render(request, 'loader/chapter.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('loader:index')

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
            return redirect('loader:login')

        if user is not None:
            login(request, user)
            return redirect('loader:index')
        else:
            messages.error(request, 'Email OR password is incorrect')

    context = {}
    return render(request, 'loader/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loader:index')


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
            return redirect('loader:index')
        else:
            messages.error(request, 'An error has occured with registration')
    context = {'form': form}
    return render(request, 'loader/register.html', context)


@login_required()
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
            return redirect('index')
    context = {'form': form}
    return render(request, 'loader/comic_form.html', context)


@login_required()
def deleteComic(request, pk):
    comic = Comic.objects.get(id=pk)
    if request.method == 'POST':
        comic.delete()
        return redirect('index')
    return render(request, 'loader/delete.html', {'obj': comic})


@login_required()
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
            return redirect('index')
    context = {'form': form}
    return render(request, 'loader/chapter_form.html', context)


@login_required()
def deleteChapter(request, pk):
    chapter = Chapter.objects.get(id=pk)
    if request.method == 'POST':
        chapter.delete()
        return redirect('index')
    return render(request, 'loader/delete.html', {'obj': chapter})


@login_required()
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    chapters = user.chapter_set.all()

    chapters_count = chapters.count()
    chapter_review = user.review_set.all()
    genres = Genre.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(chapters, 24)
    try:
        chapters = paginator.page(page)
    except PageNotAnInteger:
        chapters = paginator.page(1)
    except EmptyPage:
        chapters = paginator.page(paginator.num_pages)
    context = {'user': user, 'chapters': chapters, 'genres': genres,
               'chapters_count': chapters_count, 'chapter_review': chapter_review}
    return render(request, 'loader/profile.html', context)


@login_required()
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=pk)
    context = {'form': form}
    return render(request, 'loader/update-user.html', context)


@login_required()
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.user != review.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        review.delete()
        return redirect('loader:chapter', pk=review.chapter.id)
    return render(request, 'loader/delete.html', {'obj': review})
