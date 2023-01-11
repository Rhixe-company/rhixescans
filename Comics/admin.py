from django.contrib import admin
from .models import Comic, Chapter, Page, Genre, Review, Likes, Category

# Site Styling.
admin.site.site_header = "Rhixescans Admin"
admin.site.site_title = "Rhixescans Admin Area"
admin.site.index_title = "Welcome to the Rhixescans admin area"

# Site models.


class PageInline(admin.TabularInline):
    model = Page
    extra = 10


class ReviewInline(admin.TabularInline):
    model = Review


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 3


class ComicAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]


class ChapterAdmin(admin.ModelAdmin):
    inlines = [PageInline, ReviewInline]


admin.site.register(Comic, ComicAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Likes)
