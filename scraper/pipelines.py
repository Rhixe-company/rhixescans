# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Comics.models import *
from django.db.models import Q
from scrapy.exceptions import DropItem


class ComicsPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        if adapter.get('rating'):
            obj, created = Comic.objects.filter(
                Q(title__icontains=adapter['title']) |
                Q(slug__icontains=adapter['slug'])
            ).get_or_create(image_url=adapter['image_url'], slug=adapter['slug'], rating=adapter['rating'], status=adapter['status'], description=adapter['description'], category=adapter['category'], author=adapter['author'], release_date=adapter['release_date'], artist=adapter['artist'], defaults={'title': adapter['title'], 'slug': adapter['slug']})

            obj1, created = Genre.objects.filter(
                Q(name=adapter['genres'])
            ).get_or_create(
                name=adapter['genres'], defaults={'name': adapter['genres']})
            obj.genres.add(obj1)
            obj.save()

            return item
        if adapter.get('name'):
            comic = Comic.objects.filter(Q(title__icontains=adapter['title']) |
                                         Q(slug__icontains=adapter['slug'])).get(
                title=adapter['title'], slug=adapter['slug'])
            obj, created = Chapter.objects.filter(
                Q(name=adapter['name'])
            ).get_or_create(comics=comic, name=adapter['name'], defaults={'name': adapter['name']})
            obj1, created = Page.objects.filter(
                Q(images_url__icontains=adapter['pages'])

            ).get_or_create(images_url=adapter['pages'], defaults={'images_url': adapter['pages'], 'chapters': obj})
            obj.pages.add(obj1)

            obj.numPages = obj.page_set.all().count()
            obj.save()
            comic.numChapters = comic.chapter_set.all().count()
            comic.save()

            return item
        else:
            raise DropItem(f"Missing attribute in {item}")
