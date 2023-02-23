from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# read the input Excel file that contains the SKUs
df = pd.read_excel("input.xlsx")

skus = df["reference"].values.tolist()
prix_wiki = []
prix_spacenet = []
prix_mytek = []
driver = webdriver.Chrome("chromedriver.exe")

for i in range(0, len(skus)):
    print("Reference: ", skus[i])

    # define the URLs of the websites to scrape
    url1 = f"https://www.wiki.tn/recherche?controller=search&orderby=position&orderway=desc&search_query={skus[i]}&submit_search="
    url2 = f"https://www.mytek.tn/catalogsearch/result/?q={skus[i]}"
    url3 = f"https://spacenet.tn/recherche?controller=search&orderby=position&orderway=desc&search_query={skus[i]}"

    # wiki
    driver.get(url1)
    sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', {"class": "product_list grid row"})
    sleep(2)

    price_wiki = container.find("span", {"class": "price product-price"}).text
    print(price_wiki)
    prix_wiki.append(price_wiki)

    # mytek
    driver.get(url2)
    sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", {"class": "products wrapper list products-list"})
    sleep(2)

    try:
        price_mytek = container.find("div", {"class": "price-box price-final_price"}).findNext("span", {"class": "price"}).text
        print(price_mytek)
        prix_mytek.append(price_mytek)
    except AttributeError as a:
        prix_mytek.append("NAN")

    # space-net
    driver.get(url3)
    sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", {"class": "products"})
    sleep(2)

    try:
        for j in container.find_all("div", {"class": "item col-xs-6 col-sm-4 col-md-3 col-lg-3"}):
            ref = j.find("div", {"class": "product-reference"}).findNext("span").text
            print(ref)
            if ref == skus[i]:
                price_spacenet = j.find("div", {"class": "product-price-and-shipping"}).findNext("span", {"class": "price"}).text
                print(price_spacenet)
                prix_spacenet.append(price_spacenet)
                break
    except AttributeError as a:
        prix_spacenet.append("NAN")

output = pd.DataFrame({
    "Reference": skus,
    "Prix Wiki": prix_wiki,
    "Prix mytek": prix_mytek,
    "Prix spacenet": prix_spacenet,
})

output.to_excel("data.xlsx")
