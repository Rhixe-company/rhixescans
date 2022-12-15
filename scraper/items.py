# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from w3lib.html import remove_tags
from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Item, Field


class NewComicItem(Item):
    title = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    image_src = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(
        remove_tags))
    rating = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    artist = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    slug = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    status = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    genres = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())


class NewChapterItem(Item):
    title = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    slug = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    pages = Field(input_processor=MapCompose(
        remove_tags))
