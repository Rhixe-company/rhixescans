@login_required(login_url='login')
def scrape(request):
    if request.method == 'POST':
        with requests.Session() as s:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
            baseurl = 'https://asura.gg/manga'
            website, created = Website.objects.get_or_create(
                url=baseurl
            )

            def load(x):
                url = f'{baseurl}/?page={x}'
                r = s.get(url, headers=headers)
                html = Selector(r.text)
                return html.css('div.bs')

            def parse(articles):
                for item in articles:
                    link = item.css('a').attrib['href']
                    title = item.css('a').attrib['title']
                    r = s.get(link, headers=headers)
                    print(f'Page {link}')
                    html = Selector(r.text)
                    image = html.css("div.thumb img").attrib['src']
                    description = html.css(
                        "div.entry-content-single p::text").get().strip()
                    rating = html.css("div.num::text").get().strip()
                    category = html.css("div.tsinfo a::text").get().strip()
                    author = html.css(
                        "div.flex-wrap div.fmed span::text").get().strip()
                    genres = html.css("span.mgen a::text").getall()
                    status = html.css('div.imptdt i::text').get().strip()
                    chapters = html.css("div.chbox")
                    for chapter in chapters:
                        obj = chapter.css('a').attrib['href']
                        r = s.get(obj, headers=headers)
                        print(f'Page {obj}')
                        html = Selector(r.text)
                        name = html.css("h1.entry-title::text").get().strip()
                        posts = html.css("div.rdminimal")
                        pages = []
                        for page in posts:
                            for items in page.css('img'):
                                pages.append(str(items.attrib['src']))
                                try:
                                    alreadyExists = Comic.objects.get(
                                        title=title)
                                    genre, created = alreadyExists.genres.update_or_create(
                                        name=genres)
                                    categories, created = alreadyExists.category.update_or_create(
                                        name=category
                                    )
                                    authors, created = alreadyExists.author.update_or_create(
                                        name=author
                                    )
                                    chapter, created = Chapter.objects.get_or_create(
                                        comics=alreadyExists,
                                        website=website,
                                        name=name,
                                        user=request.user,
                                    )
                                    new_page, created = chapter.pages.get_or_create(
                                        images_url=pages,
                                        chapters=chapter
                                    )

                                except:
                                    comic, created = Comic.objects.get_or_create(
                                        title=title,
                                        rating=rating,
                                        description=description,
                                        image_url=image,
                                        status=status,
                                        website=website,
                                        user=request.user,
                                    )
                                    genre, created = comic.genres.update_or_create(
                                        name=genres)

                                    categories, created = comic.category.update_or_create(
                                        name=category
                                    )
                                    authors, created = comic.author.update_or_create(
                                        name=author
                                    )
                                    chapter, created = Chapter.objects.get_or_create(
                                        comics=comic,
                                        website=website,
                                        name=name,
                                        user=request.user,
                                    )
                                    new_page, created = chapter.pages.get_or_create(
                                        images_url=pages,
                                        chapters=chapter
                                    )

                                pass

            x = 1

            while True:
                print(f'Page {x}')
                articles = load(x)
                x = x+1

                if len(articles) != 0:
                    parse(articles)
                else:
                    break
        messages.info(request, (f'Website: {baseurl}'))
        return redirect('index')
    return render(request, 'comics/scrape.html')


@login_required(login_url='login')
def scrape(request):
    if request.method == 'POST':
        with requests.Session() as s:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
            baseurl = 'https://asura.gg/manga'
            website, created = Website.objects.get_or_create(
                url=baseurl
            )

            def load(x):
                url = f'{baseurl}/?page={x}'
                r = s.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup.find_all('div', class_='bsx')

            def parse(articles):
                comiclinks = []
                for item in articles:
                    for link in item.find_all('a', href=True):
                        comiclinks.append(link['href'])
                for link in comiclinks:
                    r = s.get(link, headers=headers)
                    print(f'Comics:{link} Status: {r.status_code}')
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        chapters = soup.find_all("div", class_='chbox')
                        try:
                            title = soup.find(
                                "h1", class_="entry-title").text.strip()
                            alreadyExists = Comic.objects.get(
                                title=title)
                        except:
                            print('title not found')
                        try:
                            rating = soup.find(
                                "div", class_="num").text.strip()
                        except:
                            print('rating not found')
                        try:
                            status = soup.find('div', class_='imptdt').find(
                                'i').text.strip()
                        except:
                            print('status not found')
                        try:
                            category = soup.find("div", class_='tsinfo').find(
                                "a").text.strip()
                        except:
                            print('category not found')
                        try:
                            image = soup.find(
                                "div", class_="thumb").find('img')['src']
                        except:
                            print('image not found')
                        try:
                            description = soup.find(
                                "div", class_='entry-content entry-content-single').find("p").text.strip()
                        except:
                            print('description not found')

                        try:
                            genree = soup.find("span", class_="mgen")
                            for objj in genree.find_all('a'):
                                genres = objj.text.strip()
                        except:
                            print('genres not found')
                        try:
                            author = soup.find("div", class_="flex-wrap").find_all(
                                'div', {'class': 'fmed'})[1].find('span').text.strip()
                        except:
                            print('author not found')
                        for page in chapters:
                            chapterlist = []
                            for link in page.find_all('a', href=True):
                                chapterlist.append(link['href'])
                                for link in chapterlist:
                                    r = s.get(link, headers=headers)
                                    print(
                                        f'Chapter:{link} Status: {r.status_code}')
                                    if r.status_code == 200:
                                        soup = BeautifulSoup(
                                            r.text, 'html.parser')
                                        posts = soup.find_all(
                                            "div", class_='rdminimal')
                                        try:
                                            name = soup.find(
                                                "h1", class_="entry-title").text.strip()
                                        except:
                                            print('name not found')
                                            pass

                                        for post in posts:
                                            for page in post.find_all("img", src=True):
                                                pages = page['src']

                                                if alreadyExists:
                                                    genre, created = alreadyExists.genres.update_or_create(
                                                        name=genres)
                                                    categories, created = alreadyExists.category.update_or_create(
                                                        name=category
                                                    )
                                                    authors, created = alreadyExists.author.update_or_create(
                                                        name=author
                                                    )
                                                    chapter, created = Chapter.objects.get_or_create(
                                                        comics=alreadyExists,
                                                        website=website,
                                                        name=name,
                                                        user=request.user,
                                                    )
                                                    new_page, created = chapter.pages.get_or_create(
                                                        images_url=pages,
                                                        chapters=chapter
                                                    )
                                                else:
                                                    comic, created = Comic.objects.get_or_create(
                                                        title=title,
                                                        rating=rating,
                                                        description=description,
                                                        image_url=image,
                                                        status=status,
                                                        website=website,
                                                        user=request.user,
                                                    )
                                                    genre, created = comic.genres.update_or_create(
                                                        name=genres)

                                                    categories, created = comic.category.update_or_create(
                                                        name=category
                                                    )
                                                    authors, created = comic.author.update_or_create(
                                                        name=author
                                                    )
                                                    chapter, created = Chapter.objects.get_or_create(
                                                        comics=comic,
                                                        website=website,
                                                        name=name,
                                                        user=request.user,
                                                    )
                                                    new_page, created = chapter.pages.get_or_create(
                                                        images_url=pages,
                                                        chapters=chapter
                                                    )
                                                pass
                                    else:
                                        print('failed')
                                        pass
            x = 1

            while True:
                print(f'Page {x}')
                articles = load(x)
                x = x+1

                if len(articles) != 0:
                    parse(articles)
                else:
                    break
        messages.info(request, (f'Website: {baseurl}'))
        return redirect('index')
    return render(request, 'comics/scrape.html')
