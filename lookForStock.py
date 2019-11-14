import requests, time

def parseMobileStock(keywords, color, size, category, qCount, proxy):
    itemId = None
    stockUrl = "https://www.supremenewyork.com/mobile_stock.json?"
    stockUrl += str(qCount)

    headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    if proxy == "":
        r = requests.get(stockUrl, headers=headers).json()
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
            }
        try:
            r = requests.get(stockUrl, headers=headers, proxies=proxies).json()
        except:
            print(f"Proxy {proxy} failed while looking for product")
            exit()

    category = category.title()

    allProdsInCat = r["products_and_categories"][category]
    for i in range(len(allProdsInCat)):
        prodName = r["products_and_categories"][category][i]["name"]
        count = 0
        for kw in keywords:
            kw = kw.upper()
            if kw in prodName.upper():
                count += 1
            else:
                break
            
        if count == len(keywords):
            itemId = r["products_and_categories"][category][i]["id"]
    return itemId

def keepLooking(KWs, clr, _siz, _cat, proxy):
    qCount = 1
    result = parseMobileStock(KWs, clr, _siz, _cat, qCount, proxy)
    while result == None:
        qCount += 1 
        time.sleep(1.5)
        print(f"Searching for keywords {KWs}")
        result = parseMobileStock(KWs, clr, _siz, _cat, qCount, proxy)
    return result

def findStyle(itemId, color, size, category, proxy):
    styleId = None
    sizeId = None
    
    if category.upper() == "tops/sweaters".upper():
        category = "tops_sweaters"
    itemUrl = f"https://www.supremenewyork.com/shop/{category}/{itemId}.json"

    headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    if proxy == "":
        r = requests.get(itemUrl, headers=headers).json()
    else:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
            }
        try:
            r = requests.get(itemUrl, headers=headers, proxies=proxies).json()
        except:
            print(f"Proxy {proxy} failed while searching for style")
            exit()
    allStyles = r["styles"]
    
    for i in range(len(allStyles)):
        colorFound = False
        sizeFound = False
        soldOut = True
        
        if r["styles"][i]["name"].upper() == color.upper():
            styleId = r["styles"][i]["id"]
            colorFound = True
            
            allSizes = r["styles"][i]["sizes"]
            for x in range(len(allSizes)):
                if r["styles"][i]["sizes"][x]["name"].upper() == size.upper():
                    sizeId = r["styles"][i]["sizes"][x]["id"]
                    sizeFound = True
                    
                    stockLevel = r["styles"][i]["sizes"][x]["stock_level"]
                    if stockLevel == 1:
                        soldOut = False

        if colorFound == True and sizeFound == True:
            if soldOut == False:
                return styleId, sizeId 
            else:
                return styleId, sizeId, "SOLD OUT"        
