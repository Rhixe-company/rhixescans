from ..items import ScraperItem, ScraperChapterItem
import scrapy
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from Comics.models import Comic, Chapter, Genre, Page


class AsuraSpider(scrapy.Spider):
    name = 'asura'

    def start_requests(self):
        yield scrapy.Request('https://asura.gg/manga/?page=1')

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)
        for x in range(2, 3):
            yield (scrapy.Request(f'https://asura.gg/manga/?page={x}', callback=self.parse))

    def parse_webtoon(self, response):
        item = ScraperItem()
        soup = BeautifulSoup(response.text, features='lxml')
        try:
            item['title'] = soup.find(
                "h1", class_="entry-title").text.strip(),
            item['image_url'] = soup.find(
                "div", class_="thumb").find('img')['src']
            item['description'] = soup.find(
                "div", class_='entry-content entry-content-single').find("p").text.strip()
            item['rating'] = soup.find(
                "div", class_="num").text.strip(),
            item['status'] = soup.find(
                "div", class_='imptdt').find('i').text.strip(),
            item['author'] = soup.find(
                "span", class_='author').text.strip(),
            item['category'] = soup.find(
                "div", class_='tsinfo').find("a").text.strip()
            item['genres'] = [genre.text.strip()
                              for genre in soup.find("span", class_="mgen").find_all('a')],
        except:
            item['title'] = soup.find(
                "h1", class_="entry-title").text.strip(),
            item['image_url'] = soup.find(
                "div", class_="thumb").find('img')['src']
            item['description'] = ''
            item['rating'] = soup.find(
                "div", class_="num").text.strip(),
            item['status'] = soup.find(
                "div", class_='imptdt').find('i').text.strip(),
            item['author'] = soup.find(
                "span", class_='author').text.strip(),
            item['category'] = soup.find(
                "div", class_='tsinfo').find("a").text.strip()
            item['genres'] = ''
        yield item
        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    def parse_chapters(self, response):
        item = ScraperChapterItem()
        soup = BeautifulSoup(response.text, features='lxml')
        try:
            item['title'] = soup.find(
                "div", class_='allc').find('a').text.strip(),
            item['name'] = soup.find(
                "h1", class_='entry-title').text.strip(),
            item['pages'] = [image['src'] for image in soup.find(
                'div', class_='rdminimal').find_all('img')]
        except:
            item['title'] = ''
            item['name'] = soup.find(
                "h1", class_='entry-title').text.strip(),
            item['pages'] = [image['src'] for image in soup.find(
                'div', class_='rdminimal').find_all('img')]
        yield item
