import requests
import time
import random
import sys

def find_id(keywords, category, size, style, proxy):
    item_id = None
    base_stock_url = "https://www.supremenewyork.com/mobile_stock.json"

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "close",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers"
    }

    while not item_id:
        print(f"searching for {keywords}")
        query_string = "?a=" + str(random.choice(range(0,1000000)))
        url = base_stock_url + query_string
        
        if not proxy:
            stock = requests.get(url, headers=headers).json()
            
        else:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}"
            }

            stock = requests.get(url, headers=headers, proxies=proxies).json()

        if parse_for_ids(stock, category, keywords):
            item_id = parse_for_ids(stock, category, keywords)
            
            style_id = None
            while not style_id:
                style_return = parse_for_styles(item_id, size, style, proxy)
                if style_return != "oos":
                    return item_id, str(style_return[0]), str(style_return[1])
            
def check_pos_neg(itemname, pos, neg):
    for p_kw in pos:
        if p_kw.lower() not in itemname:
            return False
    if neg[0]:
        for n_kw in neg:
            if n_kw.lower() in itemname:
                return False
    
    return True

def parse_for_ids(stock, category, keywords):
    positive_keywords = keywords[0]
    negative_keywords = keywords[1]

    categories = {
        "bags": "Bags",
        "pants": "Pants",
        "accessories": "Accessories",
        "skate": "Skate",
        "shoes": "Shoes",
        "hats": "Hats",
        "shirts": "Shirts",
        "sweatshirts": "Sweatshirts",
        "tops/sweaters": "Tops/Sweaters",
        "jackets": "Jackets",
        "t-shirts": "T-Shirts",
        "new" : "new"
    }
    

    value = categories.get(category.lower(), None)
    
    if value:
        category = categories[category.lower()]
    else:
        cat_list = [cat for cat in stock["products_and_categories"] if cat.lower() == category.lower()]
        if cat_list:
            category = cat_list[0]
        else:
            print("Could not find category")
            sys.exit()
        
        
    for item in stock["products_and_categories"][category]:
        itemname = item["name"].lower()
        if check_pos_neg(itemname, positive_keywords, negative_keywords):
            return item["id"]


def parse_for_styles(item_id, size, style, proxy):
    query_string = "?a=" + str(random.choice(range(0,1000000)))
    item_url = f"https://www.supremenewyork.com/shop/{item_id}.json" + query_string

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "close",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers"
    }

    if not proxy:
        styles = requests.get(item_url, headers=headers).json()
            
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }

        styles = requests.get(item_url, headers=headers, proxies=proxies).json()
    
    for stylename in styles["styles"]:
        if stylename["name"].lower() == style.lower():
            for itemsize in stylename["sizes"]:
                if itemsize["name"].lower() == size.lower():
                    if itemsize["stock_level"] != 0:
                        return itemsize["id"], stylename["id"]
                    else:
                        print("item oos, restarting")
                        return "oos"

          
    sys.exit("Could not find selected size or style")

