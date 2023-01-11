from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import files
from django.urls import reverse
from requests_html import HTMLSession
from django.utils.translation import gettext_lazy as _

# Create your models here.

s = HTMLSession()
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"
}


def comics_images_location(instance, filename):
    return '{}/{}'.format(str(instance.title).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""), filename)


def comics_chapters_images_location(instance, filename):
    return '{}/{}/{}'.format(str(instance.chapter.comic.title).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""),  instance.chapter.name, filename)


STATUS_CHOICES = [
    ('Completed', 'Completed'),
    ('Ongoing', 'Ongoing'),
    ('Dropped', 'Dropped'),
    ('Coming Soon', 'Coming Soon'),
    ('Hiatus', 'Hiatus'),
]

RATING_CHOICES = [
    (1, '1 - Trash'),
    (2, '2 - Horrible'),
    (3, '3 - Terrible'),
    (4, '4 - Bad'),
    (5, '5 - OK'),
    (6, '6 - Watchable'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Perfect'),
    (10, '10 - Master Piece'),
]


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comic(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='Ongoing')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=1000, unique=True, null=True)
    alternativetitle = models.CharField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(max_length=1000, unique=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=comics_images_location, blank=False)
    image_url = models.URLField(blank=True, null=False)
    rating = models.DecimalField(max_digits=9, decimal_places=1, blank=True)
    status = models.CharField(max_length=50)
    author = models.CharField(max_length=100, blank=True, null=True)
    artist = models.CharField(max_length=100, blank=True, null=True)
    released = models.CharField(max_length=100, blank=True, null=True)
    serialization = models.CharField(max_length=1000, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    favourites = models.ManyToManyField(
        User, blank=True, related_name='favourite')
    numChapters = models.IntegerField(default=0, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='like')
    genres = models.ManyToManyField(Genre, blank=True)
    category = models.ManyToManyField(Category)
    likes = models.ManyToManyField(
        User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    objects = models.Manager()  # default manager
    newmanager = NewManager()

    def get_absolute_url(self):
        return reverse("loader:comic", args=[self.id])

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if self.image == '' and self.image_url != '':
            resp = s.get(self.image_url,  stream=True, headers=headers)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.image_url.split("/")[-1]
            self.image.save(file_name, files.File(pb),
                            save=True)
            return super().save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        print('URL:', url)
        return url


class NewManager(models.Manager):
    pass


class ExtraManagers(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True


class ComicsManager(Comic, ExtraManagers):

    objects = NewManager()

    class Meta:

        proxy = True

    def do_something(self):
        pass


class Chapter(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, unique=True, null=True)
    pages = models.ManyToManyField('Page', blank=True, related_name='pages')
    numReviews = models.IntegerField(default=0, null=True, blank=True)
    numPages = models.IntegerField(default=0, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("loader:chapter", args=[self.id])

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    images = models.ImageField(
        upload_to=comics_chapters_images_location, max_length=10000, blank=False)
    images_url = models.URLField(
        max_length=10000, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.images)

    def save(self, *args, **kwargs):

        if self.images == '' and self.images_url != '':
            resp = s.get(self.images_url, stream=True, headers=headers)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.images_url.split("/")[-1]
            self.images.save(file_name, files.File(pb),
                             save=True)
            return super().save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        print('URL:', url)
        return url


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.SET_NULL, null=True, related_name='comments')
    text = models.TextField(max_length=3000, blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text[0:50]


class Likes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_like')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review_like')
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)
