import csv
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup


def process_price(text):
    try:
        text = str(text).replace(".", "").replace("₫", "").replace(r'\s+', "")
        return int(text)
    except:
        return "None"


def crawl_single_product(url, rv, time):
    with urllib.request.urlopen(url, timeout=time) as site:
        soup = BeautifulSoup(site.read().decode("utf8"), 'html.parser')
        _ = {}
        _['Name'] = soup.find("div", class_="product_detail-title") \
            .find("h1").string.strip()
        _['Producer'] = soup.find("ul", attrs={"class": "list-unstyled"}) \
            .contents[5].find('span', attrs={'itemprop': 'name'}).string.strip()
        summary = soup.find("div", class_="product-summary-item").find("ul")
        for child in summary.find_all("li"):
            data = [x.strip() for x in child.string.split(':')]
            if data[0] == 'Ổ cứng':
                data[0] = 'DISK'
            elif data[0] == 'VGA':
                data[0] = 'GPU'
            elif data[0] == 'Màn hình':
                data[0] = 'DISPLAY'
            _[data[0]] = data[1]
            price = soup.find("div", attrs={"id": "product-info-price"})
            _['New Price'] = process_price(price.find("strong", class_="giakm").string.strip())
            price = price.find("strong", class_="giany")
            _['Old Price'] = process_price(price.string.strip() if price else None)
            rv.append(_)


def crawl_product_list():
    res = []
    errors = []
    data = pd.read_csv('Crawl_Search_HN_CPT.csv', encoding='utf-8', sep='\t')
    data = data.loc[data["Link"] != 'None']
    urls = [x for x in data['Link']]
    for url in urls:
        print('Processed index: ', urls.index(url))
        try:
            crawl_single_product(url, res, 2)
        except:
            print(url)
            errors.append(url)
            pass

    with open('Product_HNCom.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['Name', 'Producer', 'CPU', 'RAM', 'DISK', 'GPU', 'DISPLAY', 'Old Price', 'New Price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in res:
            row = {}
            for field in fieldnames:
                row[field] = _.get(field, None)
            writer.writerow(row)
            print(row)


if __name__ == '__main__':
    crawl_product_list()
