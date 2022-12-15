import scrapy
from scrapy.spiders import Spider
from scraper.items import NewChapterItem


class ChaptersSpider(Spider):
    name = 'test'
    allowed_domains = ['asura.gg']

    def start_requests(self):

        yield scrapy.Request('https://asura.gg/manga/?page=1')

    def parse(self, response):

        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    def parse_webtoon(self, response):

        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        item = NewChapterItem()
        item['slug'] = response.css('div.bixbox ol li a ::attr(href)')[
            1].get().split("/")[-2]
        item['title'] = response.css(
            "div.allc a::text").get().strip()
        item['name'] = response.css(
            "h1.entry-title::text").get().strip()
        posts = response.css(
            "div.rdminimal img::attr(src)").getall()
        for page in posts:
            item['pages'] = page
            yield item
