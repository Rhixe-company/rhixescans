# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Comics.models import *
from django.db.models import Q
from scrapy.exceptions import DropItem


class JsonWriterPipeline:

    async def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        if adapter.get('title'):
            obj, created = Comic.objects.filter(
                Q(title=adapter['title'])
            ).get_or_create(image_url=adapter['image_url'], rating=adapter['rating'], status=adapter['status'], description=adapter['description'], category=adapter['category'], author=adapter['author'], defaults={'title': adapter['title']})
            obj1, created = Genre.objects.filter(
                Q(name=adapter['genres'])
            ).get_or_create(
                name=adapter['genres'], defaults={'name': adapter['genres']})
            obj.genres.add(obj1)
            obj.save()

            return item
        else:
            raise DropItem(f"Missing attribute in {item}")
