import requests
import time
import sys
from termcolor import colored

def get_stock(proxy):
    """
    Makes a request to Supreme's mobile_stock endpoint.
    Return its content.
    """

    url = "https://www.supremenewyork.com/mobile_stock.json"
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
        stock = requests.get(url, headers=headers).json()      
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
        stock = requests.get(url, headers=headers, proxies=proxies).json()

    return stock

def retrieve_item_id(proxy, category, positive_keywords, negative_keywords, task_name, screenlock):
    """
    Until item's id is found, get all stock and compare it
    against our positive and negative keywords.
    """

    while True:
        stock = get_stock(proxy)
        item_id = parse_for_ids(stock, category, positive_keywords, negative_keywords, task_name, screenlock)
        if item_id:
            return item_id
        
        time.sleep(0.75)
        
def retrieve_style_ids(item_id, size, style, proxy, task_name, screenlock):
    """
    Once we find the item_id, we know our item exists in Supreme's stock endpoint.
    If the item is out of stock, we waiting until it restocks.
    Otherwise, we pass off item_ids. 
    """

    oos = False
    while True:
        style_return = parse_for_styles(item_id, size, style, proxy, task_name, screenlock)
        if style_return != "oos":
            size_id = style_return[0]
            style_id = style_return[1]
            return size_id, style_id
        elif not oos:
            with screenlock:
                print(colored(f"{task_name}: Waiting for Restock", "red"))
            oos = True


def return_item_ids(positive_keywords, negative_keywords, category, size, style, proxy, task_name, screenlock):
    item_id = retrieve_item_id(proxy, category, positive_keywords, negative_keywords, task_name, screenlock)
    size_id, style_id =  retrieve_style_ids(item_id, size, style, proxy, task_name, screenlock)
    return item_id, size_id, style_id

def check_positive_keywords(itemname, positive_keywords):
    """
    Positive keywords are keywords the user wants to be in the itemname.
    For each of these keywords, if it is not in the itemname, return False.
    If we reach the end of the for loop, 
    that means all positive keywords were in the itemname and we return True.
    """

    for keyword in positive_keywords:
        if keyword.lower() not in itemname:
            return False
    return True

def check_negative_keywords(itemname, negative_keywords):
    """
    Negative keywords are opposite to positive keywords.
    First, check whether the user supplied negative keywords.
    If they did, check if they are in the itemname and return False if they are found.
    If the negative keywords are not found in the itemname,
    or there are no negative keywords, we've found the item we want,
    and return True.
    """

    if negative_keywords:
        for keywords in negative_keywords:
            if keywords.lower() in itemname:
                return False
    return True

def check_pos_neg(itemname, positive_keywords, negative_keywords):
    if check_positive_keywords(itemname, positive_keywords):
        if check_negative_keywords(itemname, negative_keywords):
            return True

def find_category_lookup_table(category):
    """
    First of two functions to find the task's category.
    Checks if the user-supplied category is in a known list of Supreme's categories.
    """

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
        return category

def find_category_with_stock(stock, task_category):
    """
    Second, much slower, function to find the task's category.
    Using list comprehension, we check if any categories from 
    Supreme's stock are equal to the supplied category,
    and return it if it is found. 
    """ 

    category_in_list = [cat for cat in stock["products_and_categories"] if cat.lower() == task_category.lower()]
    if category_in_list:
        category = category_in_list[0]
        return category
    

def return_category(stock, user_category, task_name, screenlock):
    """
    Return category if found with either find_category_lookup_table or find_category_with_stock.
    If it can't be found, stop the program as it can't go further. 
    """

    category = find_category_lookup_table(user_category)
    if category:
        return category
    else:
        category = find_category_with_stock(stock, user_category)
        if category:
            return category
        else:
            with screenlock:
                print(colored(f"{task_name}: Task exiting, category could not be found", "red"))
            sys.exit()

def parse_for_ids(stock, task_category, positive_keywords, negative_keywords, task_name, screenlock):
    """
    For each item in a specific category, check if the user's
    positive and negative keywords are within the itemname
    """

    category = return_category(stock, task_category, task_name, screenlock)
    for item in stock["products_and_categories"][category]:
        itemname = item["name"].lower()
        if check_pos_neg(itemname, positive_keywords, negative_keywords):
            return item["id"]


def get_item_variants(item_id, proxy):
    """
    Go to the item's endpoint and return its content
    """

    item_url = f"https://www.supremenewyork.com/shop/{item_id}.json" 
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
        item_variants = requests.get(item_url, headers=headers).json()
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
        item_variants = requests.get(item_url, headers=headers, proxies=proxies).json()

    return item_variants
 
def parse_for_styles(item_id, size, style, proxy, task_name, screenlock):
    """
    Get all of the different styles and colors for a specific item.
    Then attempt to find a matching size and style. 
    If unsuccessful, stop the program as it can't go further.
    """

    item_variants = get_item_variants(item_id, proxy)
    for stylename in item_variants["styles"]:
        if stylename["name"].lower() == style.lower():
            for itemsize in stylename["sizes"]:
                if itemsize["name"].lower() == size.lower():
                    if itemsize["stock_level"] != 0:
                        return itemsize["id"], stylename["id"]
                    else:
                        time.sleep(0.75)
                        return "oos"
    with screenlock:
        print(colored(f"{task_name}: Task exiting, could not find style or size", "red")) 
    sys.exit()

