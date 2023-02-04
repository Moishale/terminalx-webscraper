import csv
import httpx

from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict


@dataclass
class Product:
    brand: str
    title:  str
    price: int


def get_html(page):
    url = f'https://www.terminalx.com/men/knitwear-sweatshirts/sweatshirts?p={page}'
    resp = httpx.get(url)
    return HTMLParser(resp.text)


def parse_products(html):
    products = html.css('li.listing-product_3mjp')

    results = []
    for item in products:
        try:
            new_item = Product(
                brand=item.css_first('span').text(),
                title=item.css_first('a.title_3ZxJ').text(),
                price=item.css_first('div.final-price_8CiX').text().strip()
            )
            results.append(asdict(new_item))
        except:
            continue
    return results


def to_csv(res):
    with open('results.csv', 'a', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, fieldnames=['brand', 'title', 'price'])
        writer.writerows(res)


def main():
    for page in range(1, 100):
        html = get_html(page)
        res = parse_products(html)
        to_csv(res)


if __name__ == '__main__':
    main()
