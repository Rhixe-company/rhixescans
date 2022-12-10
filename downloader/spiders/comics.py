import scrapy
from ..items import *
from Comics.models import Comic, Chapter, Page
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
        item = NewComicItem()
        item['slug'] = response.css('div.bixbox ol li a ::attr(href)')[
            1].get().split("/")[-2]
        item['title'] = response.css(
            'h1.entry-title::text').get().strip()
        item['image_url'] = response.css('div.thumb img::attr(src)').get()
        item['rating'] = response.css(
            'div.num::text').get().strip()
        item['status'] = response.css(
            'div.imptdt i::text').get().strip()
        item['description'] = [description.strip() for description in response.css(
            'div.entry-content p::text').getall()]
        item['author'] = response.css(
            'div.flex-wrap div.fmed span::text')[1].get().strip()
        item['category'] = response.css(
            'div.imptdt a::text').get().strip()
        g = response.css("span.mgen a::text").getall()
        for genre in g:
            genres = genre
            item['genres'] = genres
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
        comic = Comic.objects.filter(
            Q(title=title)).get(title=title, slug=slug)
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
                numpages = obj.page_set.all()
                obj.numPages = len(numpages)
                obj.save()
                chapters = comic.chapter_set.all()
                comic.numChapters = len(chapters)
                comic.save()

        else:
            pass
