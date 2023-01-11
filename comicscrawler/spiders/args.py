import scrapy


class ArgsSpider(scrapy.Spider):
    name = 'args'
    allowed_domains = ['asurascans.com']
    start_urls = ['https://asurascans.com/manga']

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        #next_page = response.css('a.r::attr(href)')
        #yield from response.follow_all(next_page, self.parse)

    def add_variables(**kwargs):
        print(kwargs)
    
    def parse_webtoon(self, response):
        comics = {
            'slug': response.css('div.bixbox ol li a::attr(href)')[1].get().split('/')[-2],
            'title': response.css('h1.entry-title::text').get().strip(),
            'image': response.css('div.thumb img::attr(src)').get(),
            'rating': float(response.css('div.num::text').get().strip()),
            'status': response.css('div.imptdt i::text').get().strip(),
            'description': str(response.css('div.entry-content p::text').getall()),
            'released': response.css(
                'div.flex-wrap span.author i::text').get().strip(),
            'artist': response.css(
                    'div.flex-wrap span::text')[2].get().strip(),
            'category': response.css('div.imptdt a::text').get().strip(),
            'author': response.css(
                    'div.flex-wrap span::text')[1].get().strip(),
            'genres': response.css("span.mgen a::text").getall()
        }
        self.add_variables = (comics)
