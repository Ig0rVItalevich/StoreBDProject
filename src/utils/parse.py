import requests
from urllib import request
import json
from bs4 import BeautifulSoup

s = requests.session()
s.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101Firefox/69.0"
    }
)

count = 0
items = []

for i in range(1, 8):
    main_href = "https://iledebeaute.ru/shop/fragrance/unisex/tip-parfyumernaya_voda-iz-n3o/page{}/?perpage=72".format(
        str(i)
    )

    r = s.get(main_href)

    soup = BeautifulSoup(r.text, "html.parser")

    for text in soup.find_all(attrs={"class": "b-showcase__item"}, recursive=True):
        img = text.find_all("img", recursive=True)[0]
        try:
            href = "https://iledebeaute.ru" + text.find_all("a")[0].get("href")
            _r = s.get(href)
            soup_item = BeautifulSoup(_r.text, "html.parser")
            item = {}
            item["title"] = str(
                soup_item.find_all(
                    attrs={"class": "b-product-detail__title"}, recursive=True
                )[0]
                .find_all("meta")[0]
                .get("content")
            )[:-17]
            content = soup_item.find_all(
                attrs={"class": "b-tab__text"}, recursive=True
            )[0].find_all("p")
            _content = ""
            for p in content:
                _content += str(p.getText()) + "\n"
            item["content"] = _content
            item["price"] = str(
                soup_item.find_all(
                    attrs={"class": "b-product-price__card"}, recursive=True
                )[0].getText()
            ).replace(" ", "")[:-4]

            url = "https:" + img.get("src")
            count += 1
            request.urlretrieve(url, "./perfume/perfume_img" + str(count) + ".png")

            item["img"] = "./perfume/perfume_img" + str(count) + ".png"

            items.append(item)
        except BaseException:
            pass

with open("items.json", "w") as write_file:
    json.dump(items, write_file, indent=4, separators=(",", ": "))
