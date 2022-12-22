from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from scraper.spiders.comics import ComicsSpider
from scraper.spiders.chapters import ChaptersSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        configure_logging()
        settings = get_project_settings()
        runner = CrawlerRunner(settings)

        @defer.inlineCallbacks
        def crawl():

            yield runner.crawl(ComicsSpider)
            reactor.stop()

        crawl()
        reactor.run()
