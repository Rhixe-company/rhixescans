import scrapy
from ..items import ScraperItem, NewChapterItem
from bs4 import BeautifulSoup
from Comics.models import ComicsManager, Genre, Chapter, Page
from django.db.models import Q
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ComicsSpider(CrawlSpider):
    name = 'comics'
    allowed_domains = ['asurascans.com']
    start_urls = ['https://www.asurascans.com/manga/']
    rules = (
        Rule(LinkExtractor(allow='page')),
        Rule(LinkExtractor(allow='manga'),
             callback='parse_webtoon')
    )

    def parse_webtoon(self, response):
        for items in response.css('div#content'):
            item = ScraperItem()
            item['slug'] = items.css('div.bixbox ol li a::attr(href)')[
                1].get().split('/')[-2]
            item['title'] = items.css('h1.entry-title::text').get().strip()
            item['image_url'] = items.css('div.thumb img::attr(src)').get()
            item['rating'] = float(items.css('div.num::text').get().strip())
            item['status'] = items.css('div.imptdt i::text').get().strip()
            item['description'] = [description.strip() for description in items.css(
                'div.entry-content p::text').getall()]
            item['released'] = items.css(
                'div.flex-wrap span.author i::text').get().strip()
            item['artist'] = items.css(
                'div.flex-wrap span::text')[2].get().strip()
            item['category'] = items.css('div.imptdt a::text').get().strip()
            item['author'] = items.css(
                'div.flex-wrap span::text')[1].get().strip()

            g = items.css("span.mgen a::text").getall()
            for genre in g:
                item['genres'] = genre
                yield item
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
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
            comic = ComicsManager.objects.filter(Q(title__icontains=item['title'])).get(
                title=item['title'])
            obj, created = Chapter.objects.filter(
                Q(name=item['name'])
            ).get_or_create(comics=comic, name=item['name'], defaults={'name': item['name']})
            obj1, created = Page.objects.filter(
                Q(images_url__icontains=item['pages'])
            ).get_or_create(images_url=item['pages'], defaults={'images_url': item['pages'], 'chapters': obj})
            obj.pages.add(obj1)
            obj.numPages = obj.page_set.all().count()
            obj.save()
            comic.numChapters = comic.chapter_set.all().count()
            comic.save()
