import time
import unicodedata
from itertools import chain
import requests
from bs4 import BeautifulSoup


def get_products(args):
    def process(args_):
        url = args_[0]
        if url is None:
            return None, None
        time.sleep(2)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Pragma": "no-cache"
        }
        response = session.get(url, headers=headers)
        bsObj = BeautifulSoup(response.text, "html.parser")
        item_product = bsObj.find_all("div", {"class": "item-product"})
        for product in item_product:
            product_collection.append({
                "title": product.find("h3").text,
                "product_url": product.find("a", {"class": "product-thumbnail"})["href"],
                "image_url": product.find("img", {"data-full-size-image-url": True})["data-full-size-image-url"],
                "price": unicodedata.normalize("NFKD", product.find("span", {"class": "price"}).text),
                "brand": product.find("div", {"class": "manufacturer"}).text,
                "available": str(product.find("div", {"class": "availability-list"}).span.text).endswith("En stock"),
                "description": product.find("div", {"class": "product-desc"}).get_text(separator=" ", strip=True),
                "category": args[1],
                "site": "sbs"
            })

        next_ = bsObj.find("a", {"rel": "next"})
        next_ = next_["href"] if next_ else next_
        return next_, args_[1]

    session = requests.Session()
    session.proxies = {"http": "http://207.244.242.103:9090"}
    product_collection = list()
    url_, cat = process(args)
    while url_ is not None:
        print(url_)
        url_, cat = process((url_, cat))
    return product_collection


def extract():
    products_url = [
        ("https://sbsinformatique.com/peripheriques/accessoires-gaming-tunisie/", "peripheriques-accessoires"),
        ("https://sbsinformatique.com/composants/", "composants-stockage"),
        ("https://sbsinformatique.com/peripheriques/stockage-tunisie/", "composants-stockage"),
        ("https://sbsinformatique.com/laptops-tunisie/", "pc"),
        ("https://sbsinformatique.com/pcs-gamers-tunisie/", "pc")
    ]
    ls = map(get_products, products_url)
    return list(chain.from_iterable(ls))


if __name__ == '__main__':
    print(extract())
