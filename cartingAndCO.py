import requests, time
    
def atcCheckout(itId, styId, sizId, start, profileInfo):
    s = requests.Session()
    url = f"https://www.supremenewyork.com/shop/{itId}/add.json"

    headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        "st": styId,
        "s": sizId,
        "qty": "1"
    }

    q = s.post(url, headers=headers, data=data)
    print(q.content)
    
    # this is our checkout portion
    cooks = s.cookies.get_dict()
    cookSub = cooks["pure_cart"]
    coHeaders = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.supremenewyork.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.supremenewyork.com/mobile/',
    'TE': 'Trailers'
    }

    coData = {
        'store_credit_id': '',
        'from_mobile': '1',
        'same_as_billing_address': '1',
        'scerkhaj': 'CKCRSUJHXH',
        'order[billing_name]': '',
        'order[bn]': profileInfo["userName"],
        'order[email]': profileInfo["userEmail"],
        'order[tel]': profileInfo["userTel"],
        'order[billing_address]': profileInfo["userAddress"],
        'order[billing_address_2]': profileInfo["userApt"],
        'order[billing_zip]': profileInfo["userZip"],
        'order[billing_city]': profileInfo["userCity"],
        'order[billing_state]': profileInfo["userState"],
        'order[billing_country]': profileInfo["userCountry"],
        'carn': profileInfo["userCardNumber"],
        'credit_card[month]': profileInfo["userExpMonth"],
        'credit_card[year]': profileInfo["userExpYear"],
        'credit_card[vvv]': profileInfo["userCvv"],
        'order[terms]': '0',
        'order[terms]': '1'
    }
    s.cookies["hasShownCookieNotice"] = "1"
    s.cookies["lastVisitedFragment"] = "checkout" 
    coData["cookie-sub"] = cookSub
    coUrl = "https://www.supremenewyork.com/checkout.json"
    
    z = s.post(coUrl, headers=coHeaders, data=coData)
    end = time.time()
    allTime = end - start

    return (z.json(), allTime)

def getStatus(slug):
    statUrl = f"https://www.supremenewyork.com/checkout/{slug}/status.json"
    r = requests.get(statUrl).json()

    return r["status"]
