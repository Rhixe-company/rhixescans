from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from datetime import timezone
from django.core import files
from requests_html import HTMLSession

# Create your models here.


def comics_images_location(instance, filename):
    return '{}/{}'.format(str(instance.title).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""), filename)


def comics_chapters_images_location(instance, filename):
    return '{}/{}/{}'.format(str(instance.chapters.comics.title).replace(" ", "_").replace(":", " ").replace("/", "").replace("\\", ""),  instance.chapters.name, filename)


STATUS_CHOICES = [
    ('Completed', 'Completed'),
    ('Ongoing', 'Ongoing'),
    ('Dropped', 'Dropped'),
]

CATEGORY_CHOICES = [
    ('Manhwa', 'Manhwa'),
    ('Manhua', 'Manhua'),
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

s = HTMLSession()


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Comic(models.Model):
    reader = models.ManyToManyField(
        User, related_name='readers', blank=True)
    title = models.CharField(max_length=200, unique=True, null=False)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=comics_images_location, null=False)
    image_url = models.URLField(null=True)
    rating = models.DecimalField(
        max_digits=9, decimal_places=1, null=False)
    status = models.BooleanField(
        max_length=100, choices=STATUS_CHOICES)
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(
        max_length=100, default='Manhwa', choices=CATEGORY_CHOICES)
    genres = models.ManyToManyField(Genre, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now

    def save(self, *args, **kwargs):

        if self.image == '' and self.image_url != '':
            resp = s.get(self.image_url,  stream=True)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.image_url.split("/")[-1]
            self.image.save(file_name, files.File(pb),
                            save=True)
        else:
            return super().save(*args, **kwargs)


class Page(models.Model):
    chapters = models.ForeignKey(
        'Chapter', on_delete=models.CASCADE, related_name='Pages')
    images = models.ImageField(
        upload_to=comics_chapters_images_location, max_length=10000)
    images_url = models.URLField(null=True, max_length=10000)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.images)

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


class Chapter(models.Model):
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    comics = models.ForeignKey(Comic, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=1000, unique=True, null=False)
    pages = models.ManyToManyField(Page, blank=True, related_name='pages')
    numReviews = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=9, decimal_places=1, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now


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
