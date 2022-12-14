from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
#from Comics.comics import ComicsSpider
#from Comics.chapters import ChaptersSpider
from downloader import settings as my_settings
from Comics.comics import ComicsSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(ComicsSpider)
        process.start()
