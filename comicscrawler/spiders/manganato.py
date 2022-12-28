import scrapy
from ..items import ScraperItem,  NewChapterItem
from Comics.models import ComicsManager, Genre, Chapter, Page
from django.db.models import Q
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup


class ManganatoSpider(scrapy.Spider):
    name = 'manganato'
    allowed_domains = ['manganato.com']

    def start_requests(self):
        yield SplashRequest('https://manganato.com/genre-all')

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
            slug = response.css('a.a-h::attr(href)')[6].get().split("/")[-1]
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
            item['slug'] = slug
            item['title'] = title
            item['image_url'] = image
            item['description'] = description
            item['rating'] = rating
            item['status'] = status
            item['artist'] = artist
            item['author'] = author
            item['genres'] = genres
            yield item
        for link in response.css('div.panel-story-chapter-list ul.row-content-chapter li.a-h a.chapter-name::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        item = NewChapterItem()
        item['title'] = response.css('a.a-h::text')[1].get().strip()
        item['slug'] = response.css(
            'a.a-h::attr(href)')[1].get().split("/")[-1]
        item['name'] = str(response.css(
            'div.body-site div.panel-chapter-info-top h1::text').get().strip())
        soup = BeautifulSoup(response.text, features='lxml')
        posts = soup.select(
            "div.rdminimal img")
        for page in posts:
            item['pages'] = page['src']
            yield item
            comic = ComicsManager.objects.filter(Q(title__icontains=item['title']) |
                                                 Q(slug__icontains=item['slug'])).get(
                title=item['title'], slug=item['slug'])
            obj, created = Chapter.objects.filter(
                Q(name=item['name'])
            ).get_or_create(comics=comic, name=item['name'], defaults={'name': item['name']})
            obj1, created = Page.objects.filter(
                Q(images_url__icontains=item['pages'])
            ).get_or_create(images_url=item['pages'], defaults={'images_url': item['pages'], 'chapters': obj})
            obj.pages.add(obj1)
            obj.numPages = obj.page_set.all().count()
            obj.save()
            comic.numChapters = comic.chapter_set.all().count()
            comic.save()
