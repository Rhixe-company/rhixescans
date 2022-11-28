from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import scrapy
from .models import Comic, Chapter, Genre, Page
from django.db.models import Q


class ComicSpider(Spider):
    name = 'comics'

    def start_requests(self):
        yield scrapy.Request('https://asura.gg/manga/')

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_webtoon(self, response):
        title = response.css(
            "div.infox h1.entry-title::text").get().strip()
        image_url = response.css('div.thumb img::attr(src)').get()
        description = response.css(
            'div.wd-full div.entry-content p::text').getall()
        rating = response.css('div.num::text').get().strip()
        status = response.css('div.imptdt i::text').get()
        author = response.css(
            "span.author::text").get().strip()
        category = response.css(
            'div.imptdt a::text').get().strip()
        obj, created = Comic.objects.filter(
                        Q(title=title)
                    ).get_or_create(image_url=image_url, rating=rating, status=status, description=description, category=category, author=author, defaults={'title': title})
        g = response.css("span.mgen a::text").getall()
        for genre in g:
            genres = genre
            obj1, created = Genre.objects.filter(
                Q(name=genres)
            ).get_or_create(name=genres, defaults={'name': genres})
        obj.genres.add(obj1)
        obj.save()
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        title = response.css(
            "div.allc a::text").get().strip()
        name = response.css(
            "h1.entry-title::text").get().strip()
        comic = Comic.objects.get(title=title)
        obj, created = Chapter.objects.filter(
            Q(name=name)
        ).get_or_create(comics=comic, name=name, defaults={'name': name})
        posts = response.css(
            "div.rdminimal img::attr(src)").getall()
        for page in posts:
            pages = page
            obj1, created = Page.objects.filter(
                Q(images_url=pages)
            ).get_or_create(chapters=obj, images_url=pages, defaults={'images_url': pages})
            obj.pages.add(obj1)
            obj.save()


process = CrawlerProcess(get_project_settings())
process.crawl(ComicSpider)
process.start()
