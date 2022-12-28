# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Comics.models import ComicsManager, Genre
from django.db.models import Q
from scrapy.exceptions import DropItem


class ComicscrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('rating'):
            obj, created = ComicsManager.objects.filter(
                Q(title__icontains=adapter['title']) |
                Q(slug__icontains=adapter['slug'])
            ).get_or_create(image_url=adapter['image_url'], slug=adapter['slug'], rating=adapter['rating'], status=adapter['status'], description=adapter['description'],  author=adapter['author'],  artist=adapter['artist'], defaults={'title': adapter['title'], 'slug': adapter['slug']})
            obj1, created = Genre.objects.filter(
                Q(name=adapter['genres'])
            ).get_or_create(
                name=adapter['genres'], defaults={'name': adapter['genres']})
            obj.genres.add(obj1)
            obj.save()

            return item

        else:
            raise DropItem(f"Missing attribute in {item}")
