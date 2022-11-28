from scrapy.spiders import Spider
from ..items import ScraperItem, ScraperChapterItem
from Comics.models import Comic, Chapter, Genre, Page
from django.db.models import Q
from bs4 import BeautifulSoup


class AsuraSpider(Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']
    start_urls = ['https://asura.gg/manga/?page=1']

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        for x in range(2, 10):
            yield response.follow(f'https://asura.gg/manga/?page={x}', callback=self.parse)

    def parse_webtoon(self, response):
        item = ScraperItem()
        item['title'] = response.css(
            'h1.entry-title::text').get().strip().replace("\n", "")
        item['image_url'] = response.css('div.thumb img::attr(src)').get()
        item['rating'] = response.css(
            'div.num::text').get().strip().replace("\n", "")
        item['status'] = response.css(
            'div.imptdt i::text').get().strip().replace("\n", "")
        item['description'] = response.css(
            'div.entry-content p::text').getall()[:24]
        item['author'] = response.css(
            'span.author::text').get().strip().replace("\n", "")
        item['category'] = response.css(
            'div.imptdt a::text').get().strip().replace("\n", "")
        item['genres'] = response.css(
            'span.mgen a::text').get()

        yield item
        obj, created = Comic.objects.filter(
            Q(title=item['title'])
        ).get_or_create(image_url=item['image_url'], rating=item['rating'], status=item['status'], description=item['description'], category=item['category'], author=item['author'], defaults={'title': item['title']})

        obj1, created = Genre.objects.filter(
            Q(name=item['genres'])
        ).get_or_create(name=item['genres'], defaults={'name': item['genres']})
        obj.genres.add(obj1)
        obj.save()
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        item = ScraperChapterItem()
        item['title'] = response.css(
            "div.allc a::text").get().strip()
        item['name'] = response.css(
            "h1.entry-title::text").get().strip(),
        yield item
        soup = BeautifulSoup(response.text, features='lxml')
        posts = soup.select(
            "div.rdminimal img")
        for page in posts:
            pages = page['src']
            comic = Comic.objects.get(title=item['title'])
            obj, created = Chapter.objects.filter(
                Q(name=item['name'])
            ).get_or_create(comics=comic, name=item['name'], defaults={'name': item['name']})

            obj1, created = Page.objects.filter(
                Q(images_url=pages)
            ).get_or_create(chapters=obj, images_url=pages, defaults={'images_url': pages})
            obj.pages.add(obj1)
            obj.save()
            yield pages
