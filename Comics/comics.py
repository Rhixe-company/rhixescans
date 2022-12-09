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
            'div.flex-wrap div.fmed span::text')[1].get().strip()
        category = response.css(
            'div.imptdt a::text').get().strip()
        obj, created = Comic.objects.filter(
            Q(title=title)
        ).get_or_create(image_url=image_url, rating=rating, status=status, description=description, category=category, author=author, defaults={'title': title})
        g = response.css("span.mgen a::text").getall()
        for genre in g:
            genres = str(genre)
            obj1, created = Genre.objects.filter(
                Q(name=genres)
            ).get_or_create(
                name=genres, defaults={'name': genres})
            try:
                obj.genres.add(obj1)
                obj.save()
            except:
                print('Genres not Added')
                pass
        chapter_page_links = response.css('ul.clstyle li a::attr(href)')
        yield from response.follow_all(chapter_page_links, self.parse_chapters)

    def parse_chapters(self, response):
        title = response.css(
            "div.allc a::text").get().strip()
        name = response.css(
            "h1.entry-title::text").get().strip()
        comic = Comic.objects.get(title=title)

        try:
            obj, created = Chapter.objects.filter(
                Q(name=name)
            ).get_or_create(comics=comic, name=name, defaults={'name': name})
        except:
            print(f'This Object Not found ,pls create:{comic}')
            pass
        soup = BeautifulSoup(response.text, features='lxml')
        posts = soup.select(
            "div.rdminimal img")
        for page in posts:
            pages = page['src']
            obj1, created = Page.objects.filter(
                Q(images_url=pages)
            ).get_or_create(chapters=obj, images_url=pages, defaults={'images_url': pages})
            try:
                obj.pages.add(obj1)
                obj.save()
            except:
                print(f'{name}: already Exists')
                pass
        numpages = obj.page_set.all()
        obj.numPages = len(numpages)
        obj.save()
        chapters = comic.chapter_set.all()
        comic.numChapters = len(chapters)
        comic.save()
