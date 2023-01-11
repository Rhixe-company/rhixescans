import scrapy
from Comics.models import Comic, Genre, Category, Chapter, Page
from django.db.models import Q


class AsurascansSpider(scrapy.Spider):
    name = 'asurascans'
    start_urls = ['https://www.asurascans.com/manga/']

    def parse(self, response):
        for link in response.css('div.bsx a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_webtoon)

        next_page = response.css('a.r::attr(href)')
        yield from response.follow_all(next_page, self.parse)

    async def parse_webtoon(self, response):
        title = response.css('h1.entry-title::text').get().strip()
        alternativetitle = response.css('.wd-full span::text').get()
        slug = response.css('div.bixbox ol li a::attr(href)')[
            1].get().split('/')[-2]
        image_url = response.css('div.thumb img::attr(src)').get()
        rating = response.css('div.num::text').get().strip()
        description = [decription.strip() for decription in response.css(
            '[itemprop="description"] p::text').getall()]
        status = response.css('div.imptdt i::text').get().strip()
        released = response.css('.flex-wrap .fmed span::text')[0].get().strip()
        author = response.css('.flex-wrap .fmed span::text')[1].get().strip()
        artist = response.css('.flex-wrap .fmed span::text')[2].get().strip()
        serialization = response.css(
            '.flex-wrap .fmed span::text')[3].get().strip()
        obj, created = Comic.objects.filter(
            Q(title__contains=title) |
            Q(slug__contains=slug)
        ).get_or_create(slug=slug, image_url=image_url,  rating=float(rating), status=status, description=description, released=released,  author=author,  artist=artist, alternativetitle=alternativetitle, serialization=serialization, defaults={'title': title, 'slug': slug})
        category = response.css('.imptdt a::text').get()
        obj2, created = Category.objects.filter(
            Q(name__contains=category)
        ).get_or_create(
            name=category, defaults={'name': category})
        genres_list = response.css('.mgen a::text').getall()
        for genre in genres_list:
            obj1, created = Genre.objects.filter(
                Q(name__contains=genre)
            ).get_or_create(
                name=genre, defaults={'name': genre})
            obj.genres.add(obj1)
            obj.category.add(obj2)
            obj.save()
        yield {
            'title': title,
            'alternativetitle': alternativetitle,
            'slug': slug,
            'image_url': image_url,
            'rating': float(rating),
            'description': description,
            'status': status,
            'released': released,
            'author': author,
            'artist': artist,
            'serialization': serialization,
            'category': category,
            'genres': genres_list
        }

        for link in response.css('ul.clstyle li a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_chapters)

    async def parse_chapters(self, response):
        slug = response.css('.allc a::attr(href)').get().split("/")[-2]
        title = response.css(".allc a::text").get().strip()
        name = response.css('.entry-title::text').get().strip()
        pages = response.css('.rdminimal img::attr(src)').getall()
        for img_url in pages:
            comic = Comic.objects.filter(
                Q(title__contains=title) |
                Q(slug__contains=slug)).get(title=title)
            if comic:
                obj, created = Chapter.objects.filter(
                    Q(name__contains=name)
                ).get_or_create(comic=comic, name=name, defaults={'name': name, 'comic': comic})
                obj1, created = Page.objects.filter(
                    Q(images_url__contains=img_url)
                ).get_or_create(images_url=img_url, chapter=obj, defaults={'images_url': img_url, 'chapter': obj})
                obj.pages.add(obj1)
                obj.numPages = obj.page_set.all().count()
                obj.save()
                comic.numChapters = comic.chapter_set.all().count()
                comic.save()
        yield {
            'slug': slug,
            'title': title,
            'name': name,
            'pages': pages
        }
