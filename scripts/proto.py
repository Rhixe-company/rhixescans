
import aiohttp
from django.shortcuts import render, redirect
import httpx
import asyncio
from bs4 import BeautifulSoup
import requests


from Comics.models import *

# Create your views here.


def scrapetest(request):
    async def get_page(session, url):
        async with session.get(url) as r:
            return await r.text()

    async def get_data(session, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_page(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    async def main(urls):
        async with aiohttp.ClientSession() as session:
            data = await get_data(session, urls)
            return data

    def parse(results):
        comiclinks = []
        for html in results:
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.find_all('div', class_='bsx')
            for item in articles:
                for link in item.find_all('a', href=True):
                    comiclinks.append(link['href'])
                for link in comiclinks:
                    print(link)
                    r = requests.get(link)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    chapters = soup.find_all("div", class_='chbox')
                    try:
                        title = soup.find(
                            "h1", class_="entry-title").text.strip()

                    except:
                        print('title not found')
                        pass
                    new_title = title
                    try:
                        rating = soup.find(
                            "div", class_="num").text.strip()

                    except:
                        print('rating not found')
                        pass
                    new_rating = rating
                    try:
                        status = soup.find('div', class_='imptdt').find(
                            'i').text.strip()

                    except:
                        print('status not found')
                        pass
                    new_status = status
                    try:
                        category = soup.find("div", class_='tsinfo').find(
                            "a").text.strip()
                        new_category = category
                    except:
                        print('category not found')
                        pass
                    try:
                        image = soup.find(
                            "div", class_="thumb").find('img')['src']
                        new_image = image
                    except:
                        print('image not found')
                        pass
                    try:
                        description = soup.find(
                            "div", class_='entry-content entry-content-single').find("p").text.strip()
                        new_description = description
                    except:
                        print('description not found')
                        pass
                    try:
                        genres = soup.find(
                            "span", class_="mgen").text.strip()
                        new_genres = genres
                    except:
                        print('genres not found')
                        pass
                        comic, created = Comic.objects.get_or_create(
                            title=new_title,
                            rating=new_rating,
                            description=new_description,
                            image_url=new_image,
                            status=new_status,
                            category=new_category,
                            genres=new_genres
                        )

                        print(f'Saving Comic: {new_title}')
                        for page in chapters:
                            chapterlist = []
                            url_dictionary = {}
                            for link in page.find_all('a', href=True):
                                chapterlist.append(link['href'])
                                for link in chapterlist:
                                    r = requests.get(link)
                                    if r.status_code == 200:
                                        url_dictionary[link] = []
                                        soup = BeautifulSoup(
                                            r.text, 'html.parser')
                                        try:
                                            name = soup.find(
                                                "h1", class_="entry-title").text.strip()
                                        except:
                                            print('name not found')
                                            pass
                                        new_name = name

                                        try:
                                            images = soup.find(
                                                'div', class_='rdminimal').find_all('img')
                                        except:
                                            print('no images')
                                            pass
                                        url_dictionary[link].extend(images)
                                        cleaned_dictionary = {
                                            key: value for key, value in url_dictionary.items() if len(value) > 0}
                                        for key, images in cleaned_dictionary.items():
                                            all_images = []
                                            for image in images:
                                                source_image_url = image.attrs['src']
                                                all_images.append(
                                                    source_image_url)
                                            new_files = all_images

                                        chapter, created = Chapter.objects.get_or_create(
                                            comics=comic,
                                            name=new_name,
                                            images=new_files
                                        )
                                    else:
                                        print('failed')
                                        return

    if __name__ == '__main__':
        urls = [
            'https://asura.gg/manga/?page=1',
            'https://asura.gg/manga/?page=2',
            'https://asura.gg/manga/?page=3'
        ]
        results = asyncio.run(main(urls))
        parse(results)


def scrapetest(request):
    if request.method == 'POST':
        baseurl = 'https://asura.gg/manga'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        }

        async def log_request(request):
            print(f"Request:{request.method} {request.url}")

        async def log_response(response):
            request = response.request
            print(
                f"Response: {request.method} {request.url} - Status {response.status_code}")

        async def get_comics(x: int):
            async with httpx.AsyncClient(event_hooks={'request': [log_request], 'response': [log_response]}) as client:
                url = f'{baseurl}/?page={x}'
                r = await client.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                articles = soup.find_all('div', class_='bsx')
                for item in articles:
                    for link in item.find_all('a', href=True):
                        comiclinks.append(link['href'])
                    for link in comiclinks:
                        print(link)
                        r = await client.get(link, headers=headers)
                        soup = BeautifulSoup(r.text, 'html.parser')
                        chapters = soup.find_all("div", class_='chbox')
                        try:
                            title = soup.find(
                                "h1", class_="entry-title").text.strip()
                        except:
                            print('title not found')
                            pass
                        try:
                            rating = soup.find(
                                "div", class_="num").text.strip()
                        except:
                            print('rating not found')
                            pass
                        try:
                            status = soup.find('div', class_='imptdt').find(
                                'i').text.strip()
                        except:
                            print('status not found')
                            pass
                        try:
                            category = soup.find("div", class_='tsinfo').find(
                                "a").text.strip()
                        except:
                            print('category not found')
                            pass
                        try:
                            image = soup.find(
                                "div", class_="thumb").find('img')['src']
                        except:
                            print('image not found')
                            pass
                        try:
                            description = soup.find(
                                "div", class_='entry-content entry-content-single').find("p").text.strip()
                        except:
                            print('description not found')
                            pass
                        try:
                            genres = soup.find(
                                "span", class_="mgen").text.strip()
                        except:
                            print('genres not found')
                            pass
                        Comics = {
                            "title": title,
                            "rating": rating,
                            "category": category,
                            'status': status,
                            "description": description,
                            "image": image,
                            "genres": genres,
                        }
                        print(Comics)
                        for page in chapters:
                            chapterlist = []
                            url_dictionary = {}
                            for link in page.find_all('a', href=True):
                                chapterlist.append(link['href'])
                                for link in chapterlist:
                                    r = await client.get(link, headers=headers)
                                    if r.status_code == 200:
                                        url_dictionary[link] = []
                                        soup = BeautifulSoup(
                                            r.text, 'html.parser')
                                        try:
                                            name = soup.find(
                                                "h1", class_="entry-title").text.strip()
                                        except:
                                            print('name not found')
                                            pass
                                        try:
                                            images = soup.find(
                                                'div', class_='rdminimal').find_all('img')
                                        except:
                                            print('no images')
                                            pass
                                        url_dictionary[link].extend(images)
                                        cleaned_dictionary = {
                                            key: value for key, value in url_dictionary.items() if len(value) > 0}
                                        for key, images in cleaned_dictionary.items():
                                            all_images = []
                                            for image in images:
                                                source_image_url = image.attrs['src']
                                                all_images.append(
                                                    source_image_url)
                                        Chapters = {'name': name,
                                                    'files': all_images[0:50]}
                                        print(Chapters)
                                    else:
                                        print('failed')
                                        return

        async def main():
            tasks = []
            for x in range(1, 3):
                tasks.append(get_comics(x))
            await asyncio.gather(*tasks)
        comiclinks = []
        asyncio.run(main())
        print(len(comiclinks))
        return redirect('scrape')
    return render(request, 'comics/scrape.html')
