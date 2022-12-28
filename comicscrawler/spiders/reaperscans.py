import scrapy


class ReaperscansSpider(scrapy.Spider):
    name = 'reaperscans'
    allowed_domains = ['reaperscans.com']
    start_urls = ['https://reaperscans.com/comics']

    def parse(self, response):
        pass
