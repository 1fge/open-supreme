import requests
import sys
import time
from termcolor import colored
from .get_params import get_params

def add_to_cart(item_id, size_id, style_id, task_name, screenlock):
    """
    Add an item to cart with a specific item_id, size_id, and style_id.
    Only return session object if item added to cart properly.
    """

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
        if atc_post.json()['cart'][0]["in_stock"]:
            with screenlock:
                print(colored(f"{task_name}: Added to Cart", "blue"))
            return s 

def make_checkout_parameters(s, profile, proxy, headers):
    """
    Get the content of Supreme's mobile checkout page.
    Send content to get_params function and return its response.
    """

    if not proxy:
        checkout_page_content = s.get("https://www.supremenewyork.com/mobile/#checkout", headers=headers)
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
            }
        checkout_page_content = s.get("https://www.supremenewyork.com/mobile/#checkout", headers=headers, proxies=proxies)
    
    cookie_sub = s.cookies.get_dict()["pure_cart"]
    checkout_params = get_params(checkout_page_content.content, profile, cookie_sub)

    if not checkout_params:
        sys.exit("Error with parsing checkout parameters")
    else:
        return checkout_params

def send_checkout_request(s, profile, delay, proxy, task_name, start_checkout_time, screenlock):
    """
    Sleep for the length of the checkout delay,
    then send the checkout request with or without proxies.
    Return the content from the checkout request.
    """

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

    checkout_params = make_checkout_parameters(s, profile, proxy, headers)
    time.sleep(delay)

    if not proxy:
        checkout_request = s.post("https://www.supremenewyork.com/checkout.json", headers=headers, data=checkout_params)
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
        checkout_request = s.post("https://www.supremenewyork.com/checkout.json", headers=headers, proxies=proxies, data=checkout_params)
    total_checkout_time = round(time.time() - start_checkout_time, 2)

    with screenlock:
        print(colored(f"{task_name}: Sent Checkout Data ({total_checkout_time} seconds)", "magenta"))
    return checkout_request

def get_slug_status(s, proxy, slug):
    """
    A slug is a unique id for each potential Supreme order.
    This function goes to a url based off of the slug, and checks 
    the order status. 
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://www.supremenewyork.com/mobile/',
        'TE': 'Trailers'
    }
    status_url = f"https://www.supremenewyork.com/checkout/{slug}/status.json"

    if not proxy:
            slug_content = s.get(status_url, headers=headers).json()
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
        slug_content = s.get(status_url, headers=headers, proxies=proxies).json()

    slug_status = slug_content["status"]
    return slug_status

def display_slug_status(s, proxy, checkout_response, task_name, screenlock):
    """
    This function displays the content returned from the slug url
    until the 'status' is something other than 'queued'.
    """

    slug = checkout_response["slug"]
    while True:
        slug_status = get_slug_status(s, proxy, slug)

        with screenlock:
            if slug_status == "queued":
                print(colored(f"{task_name}: Getting Order Status", "yellow"))
            elif slug_status == "paid":
                print(colored(f"{task_name}: Check Email!", "green"))
                break
            elif slug_status == "failed":
                print(colored(f"{task_name}: Checkout Failed", "red"))
                return "failed"
        time.sleep(10)

def get_order_status(s, proxy, checkout_request, task_name, screenlock):
    """
    After sending checkout details, we check to see if the purchase
    instantly failed or if our order is queued.
    If it doesn't instantly fail, display the status of our checkout,
    otherwise restart the program.
    """
    
    checkout_response = checkout_request.json()
    if checkout_response["status"] == "failed":
        with screenlock:
            print(colored(f"{task_name}: Checkout Failed", "red"))
        return False

    elif checkout_response["status"] == "queued":
        status = display_slug_status(s, proxy, checkout_response, task_name, screenlock)
        if status != "failed":
            return True
        
def checkout(s, profile, delay, proxy, task_name, start_checkout_time, screenlock):
    """
    Send the checkout request, monitor the status of the order,
    and stop the program upon a successful purchase.
    """
    checkout_request = send_checkout_request(s, profile, delay, proxy, task_name, start_checkout_time, screenlock)
    if get_order_status(s, proxy, checkout_request, task_name, screenlock):
        return True
    

