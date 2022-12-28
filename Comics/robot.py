
from bs4 import BeautifulSoup

import requests

headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}

comiclinks = []
comiclist = []


with requests.Session() as s:

    def request(x):

        url = f'https://asura.gg/manga/?page={x}'

        r = s.get(url, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.content, features='lxml')

        return soup.find_all('div', class_='bsx')

    def parse(articles):
        for item in articles:
            for link in item.find_all('a', href=True):
                comiclinks.append(link['href'])

        for link in comiclinks:
            r = s.get(link, headers=headers)
            print(r.status_code)
            soup = BeautifulSoup(r.content, features='lxml')
            chapters = soup.find_all("div", class_='chbox')
            title = soup.find("h1", class_="entry-title").text.strip()
            rating = soup.find("div", class_="num").text.strip()
            type = soup.find("div", class_='tsinfo').find("a").text.strip()

            image = soup.find("div", class_="thumb").find('img')['src']
            try:
                description = soup.find(
                    "div", class_='entry-content entry-content-single').find("p").text.strip()
            except:
                description = "-"
            try:
                genres = soup.find("span", class_="mgen").text.strip()
            except:
                genres = '-'

                print({
                    "title": title,
                    "rating": rating,
                    "type": type,
                    "description": description,
                    "image": image,
                    "genres": genres,

                })

            for chapter in chapters:
                name = chapter.find("span", class_="chapternum").text
                chapterlist = []
                for link in chapter.find_all('a', href=True):
                    chapterlist.append(link['href'])
                    for link in chapterlist:
                        r = requests.get(link, headers=headers)
                        print(r.status_code)
                        soup = BeautifulSoup(r.text, 'html.parser')
                        posts = soup.find_all("div", class_="rdminimal")
                        for post in posts:

                            for items in post.find_all('img', src=True):
                                pages = items['src']

                                Chapters = {'name': name, 'images': pages}
                                print(Chapters)

    x = 1

    while True:
        print(f'Page {x}')
        articles = request(x)
        x = x+1

        if len(articles) != 0:
            parse(articles)
        else:
            break
