from scrapy.spiders import Spider
from .models import Comic, Chapter, Genre, Page
from django.db.models import Q
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess


class ComicSpider(Spider):
    name = 'comics'
    allowed_domains = ['asura.gg']
    start_urls = ['https://asura.gg/manga/?page=1']

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        for x in range(2, 10):
            yield response.follow(f'https://asura.gg/manga/?page={x}', callback=self.parse)

    def parse_webtoon(self, response):
        soup = BeautifulSoup(response.text, features='lxml')
        try:
            title = soup.find(
                "div", class_="infox").find('h1', class_='entry-title').text.strip().replace("\n", "")
            image_url = soup.find(
                "div", class_="thumb").find('img')['src']
            description = soup.find(
                "div", class_='entry-content entry-content-single').find("p").text.strip().replace("\n", "")
            rating = soup.find(
                "div", class_="num").text.strip().replace("\n", ""),
            status = soup.find(
                "div", class_='imptdt').find('i').text.strip().replace("\n", ""),
            author = soup.find(
                "span", class_='author').text.strip().replace("\n", ""),
            category = soup.find(
                "div", class_='tsinfo').find("a").text.strip().replace("\n", "")
            genres = response.css("span.mgen a::text").get(),
        except:
            title = soup.find(
                "div", class_="infox").find('h1', class_='entry-title').text.strip().replace("\n", "")
            image_url = soup.find(
                "div", class_="thumb").find('img')['src']
            description = ''
            rating = soup.find(
                "div", class_="num").text.strip().replace("\n", ""),
            status = soup.find(
                "div", class_='imptdt').find('i').text.strip().replace("\n", ""),
            author = soup.find(
                "span", class_='author').text.strip().replace("\n", ""),
            category = soup.find(
                "div", class_='tsinfo').find("a").text.strip().replace("\n", "")
            genres = ''
        obj, created = Comic.objects.filter(
            Q(title=title)
        ).get_or_create(image_url=image_url, rating=rating, status=status, description=description, category=category, author=author, defaults={'title': title})

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
        soup = BeautifulSoup(response.text, features='lxml')
        comic = Comic.objects.get(title=title)
        obj, created = Chapter.objects.filter(
            Q(name=name)
        ).get_or_create(comics=comic, name=name, defaults={'name': name})
        posts = soup.select(
            "div.rdminimal img")
        for page in posts:
            pages = page['src']
            obj1, created = Page.objects.filter(
                Q(images_url=pages)
            ).get_or_create(chapters=obj, images_url=pages, defaults={'images_url': pages})
            obj.pages.add(obj1)
            obj.save()


process = CrawlerProcess(settings={})

process.crawl(ComicSpider)
process.start()
