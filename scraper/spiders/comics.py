import scrapy
from ..items import *
from Comics.models import ComicsManager, Chapter, Page
from django.db.models import Q
from bs4 import BeautifulSoup


class ComicsSpider(scrapy.Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']

    def start_requests(self):
        yield scrapy.Request('https://asura.gg/manga/?page=1')

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)

        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    def parse_webtoon(self, response):
        for items in response.css('div#content'):
            item = NewComicItem()
            item['slug'] = items.css('div.bixbox ol li a::attr(href)')[
                1].get().split('/')[-2]
            item['title'] = items.css('h1.entry-title::text').get().strip()
            item['image_src'] = items.css('div.thumb img::attr(src)').get()
            item['rating'] = float(items.css('div.num::text').get().strip())
            item['status'] = items.css('div.imptdt i::text').get().strip()
            item['description'] = [description.strip() for description in items.css(
                'div.entry-content p::text').getall()]
            item['author'] = items.css(
                'div.flex-wrap span::text')[1].get().strip()
            item['artist'] = items.css(
                'div.flex-wrap span::text')[2].get().strip()
            item['category'] = items.css('div.imptdt a::text').get().strip()
            g = items.css("span.mgen a::text").getall()
            for genre in g:
                item['genres'] = genre
                yield item

        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        slug = response.css('div.bixbox ol li a ::attr(href)')[
            1].get().split("/")[-2]
        title = response.css(
            "div.allc a::text").get().strip()
        name = response.css(
            "h1.entry-title::text").get().strip()
        comic = ComicsManager.objects.filter(Q(title__icontains=title) |
                                             Q(slug__icontains=slug)).get(title=title, slug=slug)
        # 1 -  Comic exists
        if comic:
            obj, created = Chapter.objects.filter(
                Q(name=name)
            ).get_or_create(comics=comic, name=name, defaults={'name': name})
            soup = BeautifulSoup(response.text, features='lxml')
            posts = soup.select(
                "div.rdminimal img")
            for page in posts:
                pages = page['src']

                obj1, created = Page.objects.filter(
                    Q(images_url__icontains=pages)

                ).get_or_create(images_url=pages, defaults={'images_url': pages, 'chapters': obj})
                obj.pages.add(obj1)

                obj.numPages = obj.page_set.all().count()
                obj.save()
                comic.numChapters = comic.chapter_set.all().count()
                comic.save()

        else:
            pass
