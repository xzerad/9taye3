import time
import unicodedata

import requests
from bs4 import BeautifulSoup
from itertools import chain


def get_products(args):
    def process(args_):
        url = args_[0]
        if url is None:
            return
        time.sleep(1.5)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Pragma": "no-cache"
        }
        response = requests.get(url, headers=headers)
        bsObj = BeautifulSoup(response.text, "html.parser")
        ls = bsObj.find_all("td", {"class": "col-lg-10 col-sm-10 col-md-9 col-xs-10"})
        for product in ls:
            a = product.find("a", {"itemprop": "url", "class": "product-item-link"})
            brand = product.find("div", {"itemprop": "brand"})
            brand = brand.text if brand else brand
            des = product.find("div", {"itemprop": "description"})
            des = des.find(text=True).text if des else des
            img = product.parent.find("img", {"itemprop": "image"})
            price = product.find("span", {"data-price-amount": True}).text
            available = product.find("div", {"itemprop": "availability"})
            res = {
                "product_url": a["href"],
                "image_url": img["src"],
                "title": a.text,
                "brand": brand,
                "description": des,
                "price": unicodedata.normalize("NFKD", price),
                "category": args_[1],
                "available": available.text == "En stock",
                "site": "mytek"
            }
            product_collection.append(res)
        next_ = bsObj.find("a", {"class": "action next"})
        next_ = next_["href"] if next_ else next_
        return next_, args_[1]
    product_collection = list()
    url_, cat = process(args)
    while url_ is not None:
        print(url_)
        url_, cat = process((url_, cat))
    return product_collection


def extract():
    products_url = [("https://www.mytek.tn/informatique/peripheriques-accessoires.html", "peripheriques-accessoires"),
                    ("https://www.mytek.tn/informatique/composants/stockage.html", "composants-stockage"),
                    ("https://www.mytek.tn/informatique/composants/composants-informatique.html", "composants-stockage"),
                    ("https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable.html", "pc"),
                    ("https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable-pro.html", "pc"),
                    ("https://www.mytek.tn/informatique/ordinateurs-portables/ultrabook.html", "pc"),
                    ("https://www.mytek.tn/informatique/ordinateurs-portables/pc-gamer.html", "pc"),
                    ("https://www.mytek.tn/informatique/ordinateurs-portables/mac.html", "pc"),
                    ]
    ls = map(get_products, products_url)
    return list(chain.from_iterable(ls))


if __name__ == '__main__':
    print(extract())
