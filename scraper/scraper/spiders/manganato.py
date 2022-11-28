import scrapy
from ..items import ScraperItem


class ManganatoSpider(scrapy.Spider):
    name = 'manganato'

    def start_requests(self):
        yield scrapy.Request('https://manganato.com/genre-all')

    def parse(self, response):
        for link in response.css('a.genres-item-name::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)

        for x in range(2, 1392):
            yield (scrapy.Request(f'https://manganato.com/genre-all/{x}', callback=self.parse))

    def parse_webtoon(self, response):
        item = ScraperItem()
        item['title'] = response.css('div.story-info-right h1::text').get()
        item['image_url'] = response.css(
            'span.info-image img.img-loading::attr(src)').get()
        item['description'] = response.css(
            'div.panel-story-info-description::text').getall()
        # item['views'] = response.css(
        #    'span.stre-value ::text').getall()[1].strip()
        item['rating'] = response.css(
            'em#rate_row_cmd em::text').getall()[5].strip()
        item['author'] = response.css('tr a.a-h::text').getall()[0]
        # item['genres'] = response.css(
        #    'table tr td.table-value a.a-h::text').getall()[:50]

        yield item
