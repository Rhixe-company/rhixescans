from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scraper.scraper import settings as my_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from Comics.comics import ComicsSpider
from Comics.chapters import ChaptersSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        configure_logging()
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        runner = CrawlerRunner(settings=crawler_settings)

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(ComicsSpider)
            yield runner.crawl(ChaptersSpider)
            reactor.stop()

        crawl()
        reactor.run()
