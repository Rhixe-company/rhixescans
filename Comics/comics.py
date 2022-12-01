import scrapy
from .models import Comic, Genre
from django.db.models import Q


def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v = ''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v = ''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie':
                continue
            if strip_cl and k.lower() == 'content-length':
                continue
            if k in strip_headers:
                continue
            d[k] = v
    return d


class ComicsSpider(scrapy.Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']

    def start_requests(self):
        h = get_headers('''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/ap
        ng,*/*;q=0.8
        accept-encoding: gzip, deflate, br
        accept-language: en-GB,en;q=0.5
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: none
        upgrade-insecure-requests: 1
        user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10
        7.0.0.0 Safari/537.36
        ''')
        yield scrapy.Request('https://asura.gg/manga/', headers=h)

    def parse(self, response):
        h = get_headers('''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/ap
        ng,*/*;q=0.8
        accept-encoding: gzip, deflate, br
        accept-language: en-GB,en;q=0.5
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: none
        upgrade-insecure-requests: 1
        user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10
        7.0.0.0 Safari/537.36
        ''')
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(),  headers=h, callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,  headers=h, callback=self.parse)

    def parse_webtoon(self, response):
        h = get_headers('''
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/ap
        ng,*/*;q=0.8
        accept-encoding: gzip, deflate, br
        accept-language: en-GB,en;q=0.5
        sec-fetch-dest: document
        sec-fetch-mode: navigate
        sec-fetch-site: none
        upgrade-insecure-requests: 1
        user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10
        7.0.0.0 Safari/537.36
        ''')
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
