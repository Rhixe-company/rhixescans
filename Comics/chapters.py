import scrapy
from .models import Chapter, Page, Comic
from django.db.models import Q
from bs4 import BeautifulSoup


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


class ChaptersSpider(scrapy.Spider):
    name = 'chapters'

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
            yield response.follow(link.get(), headers=h, callback=self.parse_webtoon)
        next_page = response.css('a.r::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, headers=h, callback=self.parse)

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
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), headers=h, callback=self.parse_chapters)

    def parse_chapters(self, response):
        title = response.css(
            "div.allc a::text").get().strip()
        comic = Comic.objects.get(title=title)
        name = response.css(
            "h1.entry-title::text").get().strip()
        obj, created = Chapter.objects.filter(
            Q(name=name)
        ).get_or_create(comics=comic, defaults={'name': name})
        posts = response.css(
            "div.rdminimal img::attr(src)").getall()
        for page in posts:
            pages = page
            obj1, created = Page.objects.filter(
                Q(images_url=pages)
            ).get_or_create(chapters=obj, defaults={'images_url': pages})
            obj.pages.add(obj1)
            obj.save()
