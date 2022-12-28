import scrapy
from ..items import ScraperItem


class ManganatoSpider(scrapy.Spider):
    name = 'manganato'
    allowed_domains = ['manganato.com']

    def start_requests(self):
        yield scrapy.Request('https://manganato.com/genre-all')

    def parse(self, response):
        for link in response.css('a.genres-item-name::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)

        # for x in range(2, 20):
        #    yield (scrapy.Request(f'https://manganato.com/genre-all/{x}', callback=self.parse))

        next_page = response.css('div.panel-page-number a')
        yield from response.follow_all(next_page, self.parse)

    def parse_webtoon(self, response):
        content = response.css('div.panel-story-info')
        for c in content:
            title = str(c.css('h1::text').get().strip())
            image = str(c.css('img::attr(src)').get())
            description = str(
                c.css('div.panel-story-info-description::text').getall()[1].strip())
            rating = float(c.css('em::text').getall()[6])
            author = str(c.css('td.table-value a::text').getall()[0])
            artist = str(c.css('td.table-value h2::text').get())
            status = str(c.css('td.table-value::text').getall()[2])
            g = c.css('td.table-value a::text').getall()
            for genre in g:
                genres = genre
            item = ScraperItem()
            item['title'] = title
            item['image_url'] = image
            item['description'] = description
            item['rating'] = rating
            item['status'] = status
            item['artist'] = artist
            item['author'] = author
            item['genres'] = genres
            yield item
