from scraper.scraper.items import ScraperItem
import scrapy


class PropertiesSpider(scrapy.Spider):
    name = "properties"
    allowed_domains = ['asura.gg']
    start_urls = ['http://asura.gg/manga/']

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_webtoon(self, response):
        item = ScraperItem()
        item['title'] = response.css('h1.entry-title::text').get()
        item['image'] = response.css('div.thumb img::attr(src)').get()
        item['rating'] = response.css('div.num::text').get()
        item['status'] = response.css('div.imptdt i::text').get()
        item['description'] = response.css(
            'div.entry-content p::text').getall()
        item['category'] = response.css(
            'div.imptdt a::text').get()
        item['genres'] = response.css(
            'span.mgen a::text').getall()

        yield item
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

        def parse_chapters(self, response):
            item = ScraperItem()
            item['name'] = response.css('h1.entry-title::text').get()
            item['images'] = response.css(
                'div.rdminimal img::attr(src)').getall()
            yield item
