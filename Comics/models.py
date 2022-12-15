from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from datetime import timezone
from django.core import files
from requests_html import HTMLSession
from django.utils.translation import gettext_lazy as _
# Create your models here.

s = HTMLSession()


def comics_images_location(instance, filename):
    return '{}/{}'.format(str(instance.slug).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""), filename)


def comics_chapters_images_location(instance, filename):
    return '{}/{}/{}'.format(str(instance.chapters.comics.slug).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""),  instance.chapters.name, filename)


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
    name = models.CharField(max_length=1000, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return self.name


class Comic(models.Model):

    user = models.ManyToManyField(User,  blank=True)
    title = models.CharField(max_length=2000, unique=True, null=False)
    slug = models.SlugField(max_length=2000, unique=True,
                            blank=False, null=True)
    description = models.TextField(blank=True)
    CategoryType = models.TextChoices('CategoryType', 'Manhua Manhwa Manga')

    image = models.ImageField(
        upload_to=comics_images_location, blank=True)
    image_src = models.URLField(blank=False, null=True)
    rating = models.DecimalField(
        max_digits=9, decimal_places=1, blank=False, null=False)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES)
    author = models.CharField(max_length=1000, blank=True)
    artist = models.CharField(max_length=1000, blank=True)
    category = models.CharField(
        max_length=10, choices=CategoryType.choices, )
    numChapters = models.IntegerField(default=0, null=True, blank=True)
    genres = models.ManyToManyField(
        Genre, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', '-created']

    def __str__(self):
        return '%s %s' % (self.title, self.description)

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now

    def save(self, *args, **kwargs):

        if self.image == '' and self.image_src != '':

            resp = s.get(self.image_src,  stream=True)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.image_src.split("/")[-1]
            self.image.save(file_name, files.File(pb),
                            save=True)
        else:
            return super().save(*args, **kwargs)


class NewManager(models.Manager):
    release_date = models.DateField()


class ExtraManagers(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True


class ComicsManager(Comic, ExtraManagers):

    objects = NewManager()

    class Meta:
        ordering = ['updated']
        proxy = True

    def do_something(self):
        pass


class Chapter(models.Model):
    comics = models.ForeignKey(Comic, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=1000, unique=True, blank=False, null=True)
    pages = models.ManyToManyField('Page', blank=True, related_name='pages')
    numPages = models.IntegerField(default=0, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now


class Page(models.Model):
    chapters = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    images = models.ImageField(
        upload_to=comics_chapters_images_location, max_length=10000, blank=False)
    images_url = models.URLField(max_length=10000, blank=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.images) + 'Link:'+str(self.images_url)

    def save(self, *args, **kwargs):

        if self.images == '' and self.images_url != '':
            resp = s.get(self.images_url, stream=True)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.images_url.split("/")[-1]
            self.images.save(file_name, files.File(pb),
                             save=True)
        else:
            return super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=3000, blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

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
