import scrapy
from .models import Comic, Genre
from django.db.models import Q


class ComicsSpider(scrapy.Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']

    def start_requests(self):

        yield scrapy.Request('https://asura.gg/manga/')

    def parse(self, response):

        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(),   callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,   callback=self.parse)

    def parse_webtoon(self, response):

        title = response.css(
            'h1.entry-title::text').get().strip()
        image_url = response.css('div.thumb img::attr(src)').get()
        rating = response.css(
            'div.num::text').get().strip()
        status = response.css(
            'div.imptdt i::text').get().strip()
        description = [description.strip() for description in response.css(
            'div.entry-content p::text').getall()]
        author = response.css(
            'span.author::text').get().strip()
        category = response.css(
            'div.imptdt a::text').get().strip()
        obj, created = Comic.objects.filter(
            Q(title=title)
        ).get_or_create(image_url=image_url, rating=rating, status=status, description=description, category=category, author=author, defaults={'title': title})
        g = response.css("span.mgen a::text").getall()
        for genre in g:
            genres = genre
            alreadyExists = Genre.objects.filter(name=genres).exists()
            if alreadyExists:
                pass
            else:
                obj1, created = Genre.objects.filter(
                    Q(name=genres)
                ).get_or_create(comics=obj, defaults={'name': genres})
                obj.genres.add(obj1)
                obj.save()
