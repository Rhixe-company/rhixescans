from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from word2number import w2n
from Comics.models import Comic, Chapter, Genre, Page
from django.db.models import Q


class ComicPipeline(object):

    def process_item(self, item, spider):
        obj, created = Comic.objects.filter(
            Q(title=item['title'])
        ).get_or_create(image_url=item['image_url'], rating=item['rating'], status=item['status'], description=item['description'], category=item['category'], author=item['author'], defaults={'title': item['title']})

        obj1, created = Genre.objects.filter(
            Q(name=item['genres'])
        ).get_or_create(name=item['genres'], defaults={'name': item['genres']})
        obj.genres.add(obj1)
        obj.save()
        return item


class ChapterPipeline(object):

    def process_item(self, item, spider):
        comic = Comic.objects.get(title=item['title'])
        obj, created = Chapter.objects.filter(
            Q(name=item['name'])
        ).get_or_create(comics=comic, name=item['name'], defaults={'name': item['name']})
        obj1, created = Page.objects.filter(
            Q(images_url=item['pages'])
        ).get_or_create(chapters=obj, images_url=item['pages'], defaults={'images_url': item['pages']})
        obj.pages.add(obj1)
        obj.save()
        return item
