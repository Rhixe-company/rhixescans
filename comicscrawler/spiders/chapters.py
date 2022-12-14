from ..items import NewChapterItem
from bs4 import BeautifulSoup
from Comics.models import *
from django.db.models import Q
from scrapy.spiders import Spider
import scrapy
from django.contrib.postgres.search import SearchVector

class ChaptersSpider(Spider):
    name = 'chapters'
    allowed_domains = ['asurascans.com']

    def start_requests(self):
        yield scrapy.Request('https://www.asurascans.com/manga/')

    def parse(self, response):

        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    async def parse_webtoon(self, response):

        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    async def parse_chapters(self, response):
        results = []
        item = NewChapterItem()
        item['slug'] = response.css('div.bixbox ol li a ::attr(href)')[
            1].get().split("/")[-2]
        item['title'] = response.css(
            "div.allc a::text").get().strip()
        item['name'] = response.css("h1.entry-title::text").get().strip()
        soup = BeautifulSoup(response.text, features='lxml')
        posts = soup.select(
            "div.rdminimal img")
        for page in posts:
            item['pages'] = page['src']
            yield item
            results = Comic.objects.annotate(
                search=SearchVector('title','slug'),).filter(search=item['title'])
            if results is not None:
                comic = ComicsManager.objects.filter(Q(title__contains=item['title']) |
                                                     Q(slug__contains=item['slug'])).get(title=item['title'])
                obj, created = Chapter.objects.filter(
                    Q(name__contains=item['name'])
                ).get_or_create(comic=comic, name=item['name'], defaults={'name': item['name']})
                obj1, created = Page.objects.filter(
                    Q(images_url__contains=item['pages'])
                ).get_or_create(images_url=item['pages'], defaults={'images_url': item['pages'], 'chapter': obj})
                obj.pages.add(obj1)
                obj.numPages = obj.page_set.all().count()
                obj.save()
                comic.numChapters = comic.chapter_set.all().count()
                comic.save()
            else:
                self.logger.info(
                    'A chapter from %s couldnt be saved', response.url)
