from django.contrib import admin
from .models import Website, Comic, Chapter, Page, Genre, Review, Likes

# Site Styling.
admin.site.site_header = "Rhixescans Admin"
admin.site.site_title = "Rhixescans Admin Area"
admin.site.index_title = "Welcome to the Rhixescans admin area"

# Site models.
admin.site.register(Website)
admin.site.register(Comic)
admin.site.register(Chapter)
admin.site.register(Page)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Likes)
