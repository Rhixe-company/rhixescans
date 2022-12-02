import scrapy
from .models import Chapter, Page, Comic
from django.db.models import Q
from bs4 import BeautifulSoup


class ChaptersSpider(scrapy.Spider):
    name = 'chapters'

    def start_requests(self):

        yield scrapy.Request('https://asura.gg/manga/?page=1')

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

        name = response.css('div.bixbox ol li a ::attr(href)')[
            2].get().split("/")[-2]

        alreadyExists = Chapter.objects.get(
            name=name)
        try:
            posts = response.css(
                "div.rdminimal img::attr(src)").getall()
            for page in posts:
                pages = page
                obj1, created = alreadyExists.pages.get_or_create(
                    chapters=alreadyExists, defaults={'images_url': pages})
        except:
            print('pages not found')
