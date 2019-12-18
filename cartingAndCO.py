import requests, time, sys
from get_params import get_params as gparams

def atcCheckout(itId, styId, sizId, start, profileInfo, proxy):
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
    
    checkout_page = s.get("https://www.supremenewyork.com/mobile/#checkout")
    coData = gparams(profileInfo, checkout_page.content, cookSub)
    
    if coData == None:
        print("\nError with parsing checkout parameters")
        sys.exit(0)
    else:
        
        s.cookies["hasShownCookieNotice"] = "1"
        s.cookies["lastVisitedFragment"] = "checkout" 
        coUrl = "https://www.supremenewyork.com/checkout.json"
        
        if proxy == "":
            time.sleep(4.75)
            z = s.post(coUrl, headers=coHeaders, data=coData)
        else:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}"
                }
            try:
                time.sleep(4.75)
                z = s.post(coUrl, headers=coHeaders, data=coData, proxies=proxies)
            except:
                print(f"Proxy {proxy} failed at checkout")
                exit()

        end = time.time()
        allTime = end - start
        allTime = round(allTime, 3)
        allTime = f"\nCheckout details sent in {allTime} seconds"
        return (z.json(), allTime)

def getStatus(slug, proxy):
    statUrl = f"https://www.supremenewyork.com/checkout/{slug}/status.json"
    
    if proxy == "":
        r = requests.get(statUrl).json()

    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
            }
        try:
            time.sleep(4.75)
            r = requests.get(statUrl, proxies=proxies).json()
        except:
            print(f"Proxy {proxy} failed at status check")
            sys.exit(0)
    return r["status"]
