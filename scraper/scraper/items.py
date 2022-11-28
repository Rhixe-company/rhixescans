from scrapy.item import Field, Item
from w3lib.html import remove_tags
from itemloaders.processors import MapCompose, TakeFirst


def remove_white(value):
    return value.strip().replace("\n", "")


class ScraperItem(Item):
    title = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    image_url = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(
        remove_tags, remove_white))
    rating = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    genres = Field(input_processor=MapCompose(
        remove_tags, remove_white))
    status = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())


class ScraperChapterItem(Item):
    title = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(
        remove_tags, remove_white), output_processor=TakeFirst())
    pages = Field(input_processor=MapCompose(
        remove_tags, remove_white))
