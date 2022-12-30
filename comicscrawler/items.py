# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import scrapy


class ComicscrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ScraperItem(Item):
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
    artist = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    slug = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    status = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    genres = Field(input_processor=MapCompose(
        remove_tags))
    released = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    serialized = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    created = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    updated = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())


class NewChapterItem(Item):
    slug = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    pages = Field(input_processor=MapCompose(
        remove_tags))
