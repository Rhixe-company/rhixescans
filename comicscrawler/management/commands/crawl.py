from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
#from Comics.robot import ComicSpider
from comicscrawler import settings as my_settings
from comicscrawler.spiders.asurascans import AsurascansSpider
#from comicscrawler.spiders.manganato import ManganatoSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(AsurascansSpider)
        process.start()
