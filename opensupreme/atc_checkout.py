import requests
import sys
import time
from .get_params import get_params

def atc(item_id, size_id, style_id):
    s = requests.Session()
    atc_url = f"https://www.supremenewyork.com/shop/{item_id}/add.json"

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.supremenewyork.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.supremenewyork.com/mobile/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

    data = {
        "s": size_id,
        "st": style_id,
        "qty": "1" 
    }

    atc_post = s.post(atc_url, headers=headers, data=data)

    if atc_post.json():
        if atc_post.json()[0]["in_stock"]:
            return s 

    else:
        "oos or other atc problem"

def checkout(s, profile, delay, proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    cookie_sub = s.cookies.get_dict()["pure_cart"]

    if not proxy:
        checkout_page_content = s.get("https://www.supremenewyork.com/mobile/#checkout", headers=headers)
    
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
            }
        checkout_page_content = s.get("https://www.supremenewyork.com/mobile/#checkout", headers=headers, proxies=proxies)
    
    checkout_params = get_params(checkout_page_content.content, profile, cookie_sub)

    if not checkout_params:
        sys.exit("Error with parsing checkout parameters")

    else:
        time.sleep(delay)

        if not proxy:
            checkout_post = s.post("https://www.supremenewyork.com/checkout.json", headers=headers, data=checkout_params)
        
        else:
            checkout_post = s.post("https://www.supremenewyork.com/checkout.json", headers=headers, proxies=proxies, data=checkout_params)

        checkout_response = checkout_post.json()
        if checkout_response["status"] == "failed":
            print("Checkout Failed")
            return False

        elif checkout_response["status"] == "queued":
            slug = checkout_response["slug"]
            status_url = f"https://www.supremenewyork.com/checkout/{slug}/status.json"

            for _ in range(3):
                if not proxy:
                    stat = requests.get(status_url).json()
                else:
                    stat = requests.get(status_url, proxies=proxies).json()
                    
                time.sleep(3.5)
                print(f"Checkout Status: {stat['status']}")
            
            return True

