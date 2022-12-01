import scrapy
from .models import Chapter, Page, Comic
from django.db.models import Q


class ChaptersSpider(scrapy.Spider):
    name = 'chapters'

    def start_requests(self):

        yield scrapy.Request('https://asura.gg/manga/')

    def parse(self, response):

        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_webtoon(self, response):

        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        title = response.css(
            "div.allc a::text").get().strip()
        comic = Comic.objects.get(title=title)
        name = response.css(
            "h1.entry-title::text").get().strip()
        obj, created = Chapter.objects.filter(
            Q(name=name)
        ).get_or_create(comics=comic, defaults={'name': name})
        posts = response.css(
            "div.rdminimal img::attr(src)").getall()
        for page in posts:
            pages = page
            obj1, created = Page.objects.filter(
                Q(images_url=pages)
            ).get_or_create(chapters=obj, defaults={'images_url': pages})
            obj.pages.add(obj1)
            obj.save()
