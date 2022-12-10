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
