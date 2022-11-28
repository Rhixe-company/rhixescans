@login_required(login_url='login')
def scrape(request):
    comics = Comic.objects.all()
    reviews = Review.objects.all()
    if request.method == 'POST':
        baseurl = 'https://asura.gg/manga'
        website, created = Website.objects.get_or_create(
            url=baseurl
        )

        def get_page_links(url):
            r = s.get(url)
            sp = BeautifulSoup(r.content, features='lxml')
            links = sp.select('div.bsx a')
            return [link.attrs['href'] for link in links]

        def comic_data(url):
            r = s.get(url)
            sp = BeautifulSoup(r.content, features='lxml')
            chapterlist = []
            try:
                title = sp.select_one("h1.entry-title").text.strip(),
                image_url = sp.select_one("div.thumb img")['src'],
                description = sp.select_one(
                    "div.entry-content p").text.strip(),
                rating = float(sp.select_one("div.num").text.strip()),
                status = sp.select_one(
                    "div.imptdt i").text.strip(),
                author = sp.select_one(
                    "span.author").text.strip(),
                category = sp.select_one("div.tsinfo a").text.strip(),
                genres = [genre.text.strip()
                          for genre in sp.select("span.mgen a")],

            except:
                title = sp.select_one("h1.entry-title").text.strip(),
                image_url = sp.select_one("div.thumb img")['src'],
                description = ''
                rating = float(sp.select_one("div.num").text.strip()),
                status = sp.select_one(
                    "div.imptdt i").text.strip(),
                author = sp.select_one(
                    "span.author").text.strip(),
                category = sp.select_one("div.tsinfo a").text.strip(),
                genres = [genre.text.strip()
                          for genre in sp.select("span.mgen a")],
            comics, created = Comic.objects.get_or_create({'user': request.user, 'website': website, 'title': title, 'image_url': image_url,
                                                           'description': description, 'rating': rating, 'status': status, 'author': author, 'category': category})
            Genres, created = Genre.objects.get_or_create({'name': genres})

        def main():
            results = []
            x = 1
            while True:
                urls = get_page_links(f'{baseurl}/?page={x}')
                comicinfo = [comic_data(url) for url in urls]
                results.append(comicinfo)
                print(f'Page{x} Completed.')
                x = x+1
                if len(comicinfo) != 0:
                    results.append(comicinfo)
                else:
                    break
            return results

        main()
        messages.info(request, (f'Website: {baseurl}'))
        return redirect('scrape')
    context = {'comics': comics, 'reviews': reviews}
    return render(request, 'comics/scrape.html', context)
