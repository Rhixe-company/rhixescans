import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
# .split("/")[-2]


class ChaptersSpider(Spider):
    name = 'chapters'
    allowed_domains = ['asura.gg']

    def start_requests(self):

        yield scrapy.Request('https://asura.gg/manga/?page=1')

    def parse(self, response):

        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    def parse_webtoon(self, response):
        slug = response.css('div.bixbox ol li a ::attr(href)')[
            1].get().split("/")[-2]
        title = response.css(
            'h1.entry-title::text').get().strip()
        print(slug, title)
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):

        slug = response.css('div.bixbox ol li a ::attr(href)')[
            1].get().split("/")[-2]
        title = response.css(
            "div.allc a::text").get().strip()
        print(slug, title)


settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(ChaptersSpider)
process.start()
