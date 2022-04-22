import time
from itertools import chain
import requests
from bs4 import BeautifulSoup
import unicodedata


def get_products(args):
    def process(args_):
        url = args_[0]
        if url is None:
            return None, None
        time.sleep(1.5)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Pragma": "no-cache"
        }
        response = session.get(url, headers=headers)
        bsObj = BeautifulSoup(response.text, "html.parser")
        section = bsObj.find("section", {"id": "center_column"})
        product_container__ = section.find_all("div", {"class": "product-container"}) if section else []
        for product in product_container__:
            a = product.find("a", {"class": "product-name"})
            title = str(a["title"]).upper()
            brand = list(filter(lambda x: x in title, brand_list))
            product_collection.append({
                "title": a["title"],
                "product_url": a["href"],
                "image_url": product.find("img", {"class": "replace-2x img-responsive"})["src"],
                "price": str(product.find("span", {"class": "product-price"}).text).strip(),
                "brand": brand[0] if len(brand) > 0 else "Unknown",
                "available": str(product.find("span", {"class": "label label-success"}).text).endswith("En stock"),
                "description": unicodedata.normalize("NFKD", product.find("div", {"class": "product-desc"}).get_text(strip=True)),
                "category": args[1],
                "site": "skymil"
            })

        next_ = bsObj.find("li", {"id": "pagination_next_bottom"})
        next_ = next_.a if next_ else next_
        next_ = next_["href"] if next_ else next_
        return next_, args_[1]
    session = requests.Session()
    session.proxies = {"http": "http://207.244.242.103:9090"}
    brand_list = ['ABKONCORE', 'ACER', 'ADVANCE', 'AERCOOL', 'AMD', 'ANTEC', 'AOC', 'APPROX', 'ARCTIC', 'ARKTEK',
                  'ASROCK', 'ASUS', 'AVERMEDIA', 'AZZATEK', 'BALLISTIX', 'BE-QUIET', 'BELKIN', 'BENQ', 'BIOSTAR',
                  'BITFENIX', 'COOLERMASTER', 'CORSAIR', 'COUGAR', 'CRUCIAL', 'D-LINK', 'DEEPCOOL', 'DELL', 'EMTEC',
                  'EVGA', 'FOXCONN', 'FSP', 'G.SKILL', 'GAINWARD', 'GAMEMAX', 'GEIL', 'GENESIS', 'GIGABYTE',
                  'GLORIOUS PC GAMING RACE', 'GOODRAM', 'HITACHI', 'HORI', 'HP', 'HYPERX', 'IIYAMA', 'INTEL',
                  'INTER-TECH', 'JONSBO', 'KEEP OUT GAMING', 'KINGSTON', 'KOLINK', 'KONIX', 'LC-POWER', 'LENOVO',
                  'LEXAR', 'LG', 'LIAN LI', 'LOGITECH', 'M.RED', 'MATROX', 'MICROSOFT', 'MIPS', 'MSI GAMING',
                  'NINTENDO', 'NJOY', 'NVIDIA', 'NZXT', 'PALIT', 'PATRIOT MEMORY', 'PHANTEKS', 'PHILIPS', 'PINNACLE',
                  'PNY', 'POINT OF VIEW', 'RAIDMAX', 'RAIJINTEK', 'RAZER GAMING', 'REBORNLEAGUE', 'REDRAGON', 'REMAX',
                  'SAMSUNG', 'SANDBERG', 'SAPPHIRE', 'SEAGATE', 'SEASONIC', 'SHARKOON', 'SILICON POWER', 'SILVERSTONE',
                  'SKYMIL-INFORMATIQUE', 'SONY', 'SPIRIT OF GAMER', 'STEELSERIES', 'SUPERTAB', 'T-DAGGER',
                  'TEAM GROUP', 'THERMALTAKE', 'TOSHIBA', 'TRANSCEND', 'TRUST GAMING', 'UNV', 'WESTERN DIGITAL']

    product_collection = list()
    url_, cat = process(args)
    base_url = "https://skymil-informatique.com"
    while url_ is not None:
        url_, cat = process((f"{base_url}{url_}", cat))
    return product_collection


def extract():
    products_url = [
        ("https://skymil-informatique.com/82-peripheriques-gaming", "peripheriques-accessoires"),
        ("https://skymil-informatique.com/18-Tunisie-composants-pc", "composants-stockage"),
        ("https://skymil-informatique.com/14-pc-gamer", "pc"),
    ]
    ls = map(get_products, products_url)
    return list(chain.from_iterable(ls))


if __name__ == '__main__':
    print(extract())
