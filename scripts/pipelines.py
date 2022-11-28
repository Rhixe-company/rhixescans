from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from word2number import w2n


class ScraperPipeline(object):

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('title'):
            item.save()
            return item
        else:
            raise DropItem(f"Missing attribute in {item}")


class RatingPipeline(object):

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('rating'):
            item['rating'] = w2n.word_to_num(item['rating'])
            return item
        else:
            raise DropItem(f"Missing rating in {item}")
