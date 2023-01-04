from ..items import ScraperItem
from Comics.models import ComicsManager,  Genre
from django.db.models import Q
from scrapy.spiders import Spider
import scrapy


class ComicsSpider(Spider):
    name = 'comics'
    allowed_domains = ['asurascans.com']

    def start_requests(self):
        yield scrapy.Request('https://www.asurascans.com/manga/')

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)

        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    async def parse_webtoon(self, response):
        for items in response.css('div#content'):
            item = ScraperItem()
            item['slug'] = items.css('div.bixbox ol li a::attr(href)')[
                1].get().split('/')[-2]
            item['title'] = items.css('h1.entry-title::text').get().strip()
            item['image_url'] = items.css('div.thumb img::attr(src)').get()
            item['rating'] = float(items.css('div.num::text').get().strip())
            item['status'] = items.css('div.imptdt i::text').get().strip()
            item['description'] = [description.strip() for description in items.css(
                'div.entry-content p::text').getall()]
            item['released'] = items.css(
                'div.flex-wrap span.author i::text').get().strip()
            item['artist'] = items.css(
                'div.flex-wrap span::text')[2].get().strip()
            item['category'] = items.css('div.imptdt a::text').get().strip()
            item['author'] = items.css(
                'div.flex-wrap span::text')[1].get().strip()
            g = items.css("span.mgen a::text").getall()
            for genre in g:
                item['genres'] = genre
                yield item
                obj, created = ComicsManager.objects.filter(
                    Q(title__icontains=item['title'])
                ).get_or_create(image_url=item['image_url'],  rating=item['rating'], status=item['status'], description=item['description'], released=item['released'], category=item['category'],  author=item['author'],  artist=item['artist'], defaults={'title': item['title']})
                obj1, created = Genre.objects.filter(
                    Q(name=item['genres'])
                ).get_or_create(
                    name=item['genres'], defaults={'name': item['genres']})
                obj.genres.add(obj1)
                obj.save()
        