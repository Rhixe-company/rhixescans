# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem, Field
from Comics.models import *
from w3lib.html import remove_tags
from itemloaders.processors import MapCompose, TakeFirst


class ComicItem(DjangoItem):
    django_model = Comic


class NewComicItem(ComicItem):
    title = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    image_url = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(
        remove_tags))
    rating = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    slug = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    status = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    genres = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())


class NewChapterItem(ComicItem):
    name = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    pages = Field(input_processor=MapCompose(
        remove_tags),)
