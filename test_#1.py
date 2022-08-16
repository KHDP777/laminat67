import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import json
import csv
# url = "https://laminat67.ru/"
#
headers = {
    "Accept": "image/avif,image/webp,*/*",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
}
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
print(soup.title)
all_hrefs = soup.find_all(class_="container-image-and-badge")
all_new_hrefs = soup.find_all(class_="product-image")
all_caterories = {}
keys = []
values = []

# for items in all_new_hrefs:
#     print(items)

for items in all_hrefs:
    name = items.img
    txt = name.get("alt")
    keys.append(txt)
    # src = name.get("src")

for items in all_new_hrefs:
    name = items.a
    href = name.get("href")
    values.append(href)

for i in range(len(keys)):
    all_caterories[keys[i]] = values[i]

with open("datebase.json", "w") as file:
    json.dump(all_caterories, file, indent=4, ensure_ascii=False)

with open("datebase.json") as file:
    all_caterories = json.load(file)

with open("all_date.json", "w") as file:
    json.dump("All DATES", file, indent=4, ensure_ascii=False)

# считаем количество итераций
iteration = int(len(all_caterories)) - 1
print(f"Всего итераций {iteration}")

# print(all_caterories)
count = 0
for name_category, href_category in all_caterories.items():

    # if count == 0:
    rep = [" ", "-"]
    for item in rep:
        if item in name_category:
            name_category = name_category.replace(item, "_")
    # print(name_category)

    req = requests.get(url=href_category, headers=headers)
    src = req.text

    with open(f"date/{count}_{name_category}.html", "w") as file:
        file.write(src)
    with open(f"date/{count}_{name_category}.html") as file:
       src = file.read()
    soup = BeautifulSoup(src, "lxml")

    # alert_block = soup.find(class_="alert_block")
    # if alert_block is not None:
    #     continue
    date = {}
    # собираем заголовки таблицы
    table_head = soup.find(class_="woocommerce-product-attributes shop_attributes table table-striped").find_all("tr")
    # print(table_head)
    for elements in table_head:
        name = elements.find("th", class_="woocommerce-product-attributes-item__label").text
        info = elements.find("a").text
        date[name] = info
    # print(date)

    with open("all_date.json", "a") as file:
        json.dump(f"{name_category}", file, indent=4, ensure_ascii=False)
        json.dump(date, file, indent=4, ensure_ascii=False)

    with open(f"date/{count}_{name_category}.csv", "w", encoding="utf-8") as file:
        writer  = csv.writer(file)
        # for name, info in date.items():
        #     print(name, info)
        #     writer.writerow(
        #         name
        #     )
        writer.writerow(
            date.keys()
        )
        writer.writerow(
            date.values()
        )
        # for name, info in date:
        #     writer.writerow(
        #         info
        #     )
    count += 1
    if iteration == 0:
        print("Все")
    else:
        print(f"Итерация {count}_{name_category} записан...")
    sleep(random.randrange(2, 4))