import scrapy
from .models import Comic, Genre, Chapter, Page
from django.db.models import Q
from bs4 import BeautifulSoup


class ComicsSpider(scrapy.Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']

    def start_requests(self):

        yield scrapy.Request('https://asura.gg/manga/?page=1')

    def parse(self, response):
        comic_page_links = response.css('div.bsx a::attr(href)')
        yield from response.follow_all(comic_page_links, self.parse_webtoon)

        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

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
        chapters = response.css('ul.clstyle')
        for c in chapters:
            n = c.css('li a::attr(href)').getall()
            for name in n:
                names = name.split("/")[-2]
                obj2, created = Chapter.objects.filter(
                    Q(name=name)
                ).get_or_create(comics=obj, name=names, defaults={'name': names})
        chapter_page_links = response.css('ul.clstyle li a::attr(href)')
        yield from response.follow_all(chapter_page_links, self.parse_chapters)

    def parse_chapters(self, response):
        soup = BeautifulSoup(response.text, features='lxml')
        name = response.css('div.bixbox ol li a ::attr(href)')[
            2].get().split("/")[-2]
        alreadyExists = Chapter.objects.get(
            name=name)
        posts = soup.select(
            "div.rdminimal img")
        for page in posts:
            pages = page['src']
            obj, created = alreadyExists.pages.get_or_create(
                chapters=alreadyExists, images_url=pages, defaults={'images_url': pages})
