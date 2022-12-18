from rest_framework import serializers
from .models import Comic, Chapter, Genre, Page
from django.contrib.auth.models import User
from users.serializers import UserSerializer


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['images']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class ChapterSerializer(serializers.ModelSerializer):
    pages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chapter
        fields = '__all__'

    def get_pages(self, obj):
        pages = obj.pages.all()
        serializer = PageSerializer(pages, many=True)
        return serializer.data


class ComicSerializer(serializers.ModelSerializer):
    readers = serializers.SerializerMethodField(read_only=True)
    genres = serializers.SerializerMethodField(read_only=True)
    chapters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comic
        fields = '__all__'

    def get_genres(self, obj):
        genres = obj.genres.all()
        serializer = GenreSerializer(genres, many=True)
        return serializer.data

    def get_readers(self, obj):
        readers = obj.reader.all()
        serializer = UserSerializer(readers, many=True)
        return serializer.data

    def get_chapters(self, obj):
        chapters = obj.chapter_set.all()
        serializer = ChapterSerializer(chapters, many=True)
        return serializer.data
