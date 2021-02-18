import sys
import time
import requests
from termcolor import colored
from .get_params import get_params

def add_to_cart(session, item_id, size_id, style_id, atc_chk, task_name, screenlock):
    """
    Add an item to cart with a specific item_id, size_id, and style_id.
    Only return session object if item added to cart properly.

    Returns:
        requests.Session, bool: Our requests.session along with a bool to designate if ATC success
    """

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
        "qty": "1",
        "chk": atc_chk
    }
    atc_url = f"https://www.supremenewyork.com/shop/{item_id}/add.json"

    while True: # keep making checkout post until 200 response
        atc_response = session.post(atc_url, headers=headers, data=data)
        if atc_response.status_code == 200:
            break
        session.event.wait(timeout=1.25)

    atc_json = atc_response.json()
    if atc_json and atc_json["cart"] and atc_json["cart"][0]["in_stock"]:
        with screenlock:
            print(colored(f"{task_name}: Added to Cart", "blue"))
        return session, True
    return session, False

def make_checkout_parameters(session, profile, headers):
    """
    Get the content of Supreme's mobile checkout page.
    Send content to get_params function and return its response.
    """

    checkout_page_content = session.get("https://www.supremenewyork.com/mobile/#checkout", headers=headers)
    cookie_sub = session.cookies.get_dict()["pure_cart"].split("%2C%22cookie")[0] + "%7D" # convert encoded {"xxxxx":1,"cookie":"1+item--xxxxx,yyyyy"} -> {"xxxxx":1}
    checkout_params = get_params(checkout_page_content.content, profile, cookie_sub)

    if not checkout_params:
        sys.exit("Error with parsing checkout parameters")
    return checkout_params

def fetch_captcha(session, checkout_params, task_name, screenlock):
    with screenlock:
        print(colored(f"{task_name}: Waiting for Captcha...", "cyan"))

    while True:
        try:
            captcha_response = session.get("http://127.0.0.1:5000/www.supremenewyork.com/token", timeout=0.1)
            if captcha_response.status_code == 200:
                return captcha_response.text
        except requests.exceptions.Timeout:
            pass

def send_checkout_request(session, profile, delay, task_name, start_checkout_time, screenlock):
    """
    Sleep for the length of the checkout delay,
    then send the checkout request.
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
    checkout_url = "https://www.supremenewyork.com/checkout.json"
    checkout_params = make_checkout_parameters(session, profile, headers)
    checkout_params["g-recaptcha-response"] = fetch_captcha(session, checkout_params, task_name, screenlock)

    with screenlock:
        print(colored(f"{task_name}: Waiting Checkout Delay...", "yellow"))
    session.event.wait(timeout=delay)

    while True: # keep sending checkout request until 200 status code
        checkout_request = session.post(checkout_url, headers=headers, data=checkout_params)
        if checkout_request.status_code == 200:
            total_checkout_time = round(time.time() - start_checkout_time, 2)
            with screenlock:
                print(colored(f"{task_name}: Sent Checkout Data ({total_checkout_time} seconds)", "magenta"))
            return checkout_request
        session.event.wait(timeout=1.25)

def get_slug_status(session, slug):
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

    slug_content = session.get(status_url, headers=headers).json()
    slug_status = slug_content["status"]
    return slug_status

def display_slug_status(session, checkout_response, task_name, screenlock):
    """
    This function displays the content returned from the slug url
    until the 'status' is something other than 'queued'.
    """

    slug = checkout_response["slug"]
    while True:
        slug_status = get_slug_status(session, slug)

        with screenlock:
            if slug_status == "queued":
                print(colored(f"{task_name}: Getting Order Status", "yellow"))
            elif slug_status == "paid":
                print(colored(f"{task_name}: Check Email!", "green"))
                break
            elif slug_status == "failed":
                print(colored(f"{task_name}: Checkout Failed", "red"))
                return "failed"
        session.event.wait(timeout=10)

def get_order_status(session, checkout_request, task_name, screenlock):
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
        status = display_slug_status(session, checkout_response, task_name, screenlock)
        if status != "failed":
            return True

def checkout(session, profile, delay, task_name, start_checkout_time, screenlock):
    """
    Send the checkout request, monitor the status of the order,
    and stop the program upon a successful purchase.
    """
    checkout_request = send_checkout_request(session, profile, delay, task_name, start_checkout_time, screenlock)
    if get_order_status(session, checkout_request, task_name, screenlock):
        return True


