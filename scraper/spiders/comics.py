import scrapy
from ..items import *
from bs4 import BeautifulSoup
from scrapy.spiders import Spider


class ComicsSpider(Spider):
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
            item['image_url'] = items.css('div.thumb img::attr(src)').get()
            item['rating'] = float(items.css('div.num::text').get().strip())
            item['status'] = items.css('div.imptdt i::text').get().strip()
            item['description'] = [description.strip() for description in items.css(
                'div.entry-content p::text').getall()]
            item['author'] = items.css(
                'div.flex-wrap span::text')[1].get().strip()
            item['artist'] = items.css(
                'div.flex-wrap span::text')[2].get().strip()
            item['category'] = items.css('div.imptdt a::text').get().strip()
            item['release_date'] = items.css(
                'div.flex-wrap span time::text').get().strip()
            g = items.css("span.mgen a::text").getall()
            for genre in g:
                item['genres'] = genre
                yield item
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
