import requests
from bs4 import BeautifulSoup


source = requests.get("http://192.168.99.233/").text
soup = BeautifulSoup(source, "html.parser")

name = soup.find('meta', {"property": "og:title"})[
    'content']


print({
    'name': name,
    'img': img,
    'price': price,
    'price_symbol': priceSymbol,
    'description': description
})
