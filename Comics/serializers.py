from rest_framework import serializers
from .models import Comic, Chapter, Genre, Page
from accounts.models import Profile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','avatar', 'bio']

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
    bookmark = serializers.SerializerMethodField(read_only=True)
    genres = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comic
        fields = '__all__'

    def get_genres(self, obj):
        genres = obj.genres.all()
        serializer = GenreSerializer(genres, many=True)
        return serializer.data

    def get_bookmark(self, obj):
        bookmark = obj.favourites.all()
        serializer = UserSerializer(bookmark, many=True)
        return serializer.data
