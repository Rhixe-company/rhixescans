from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider


class ComicSpider(Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']
    start_urls = ['https://asura.gg/manga/']

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        for x in range(2, 9):
            yield response.follow(f'https://asura.gg/manga/?page={x}', callback=self.parse)

    def parse_webtoon(self, response):
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)
        title = response.css('h1.entry-title::text').get().strip()
        image = response.css('div.thumb img::attr(src)').get().strip()
        rating = response.css('div.num::text').get().strip()
        status = response.css('div.imptdt i::text').get().strip()
        description = response.css(
            'div.entry-content p::text').getall()
        category = response.css(
            'div.imptdt a::text').get().strip()
        genres = response.css('div.wd-full span.mgen a::text').getall()
        author = response.css(
            'div.flex-wrap span::text').getall()[2].strip()
        yield {
            'title': title,
            'image': image,
            'rating': rating,
            'status': status,
            'description': description,
            'category': category,
            'genres': genres,
            'author': author
        }

    def parse_chapters(self, response):
        name = response.css('h1.entry-title::text').get().strip()
        pages = response.css('div.rdminimal img::attr(src)').getall()
        yield {
            'name': name,
            'pages': pages
        }


process = CrawlerProcess(settings={
    'FEED_URI': 'comics.json',
    'FEED_FORMAT': 'json'
})

process.crawl(ComicSpider)
process.start()
