from bs4 import BeautifulSoup


def get_data(data):
    soup = BeautifulSoup(data, "html.parser")

    h1 = soup.find('h1')
    if h1 is not None:
        h1 = h1.get_text()

    title = soup.title.string if soup.title else None

    descript = soup.find('meta', attrs={"name": "description"})
    description = descript.get('content') if descript else None
    return {'h1': h1, 'title': title, 'description': description}
