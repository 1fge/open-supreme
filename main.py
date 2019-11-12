import time, json
from multiprocessing import Process

from lookForStock import keepLooking as kl
from lookForStock import findStyle as fs
from cartingAndCO import atcCheckout as cartCO
from cartingAndCO import getStatus as gs
from getProfiles import getUsers as gu

with open("tasks.json", "r") as f:
        tasks = json.load(f)
def go(keywords, color, size, category, profileInformation, taskName):
        start = time.time()
        itemId = kl(keywords, color, size, category)
        returnedIds = fs(itemId, color, size, category)


        if returnedIds == None:
            print(f"Error finding style or size for task '{taskName}'\n")
        elif len(returnedIds) == 2:
             styleId = returnedIds[0]
             sizeId = returnedIds[1]

             result = cartCO(itemId, styleId, sizeId, start, profileInformation)
             print(result[0], result[1])
             
             if "slug" in result[0]:
                 slug = result[0]
                 slug = slug["slug"]
                 print("\n")
                 for _ in range(2):
                     stat = gs(slug)
                     time.sleep(3.5)
                     print(f"Status for '{taskName}': {stat}")
             else:
                 print(f"Checkout failed for task '{taskName}', restarting\n")
                 time.sleep(1.25)
                 go(keywords, color, size, category, profileInformation, taskName)
        else:
            print(f"Item sold out for '{taskName}', restarting")
            time.sleep(2)
            go(keywords, color, size, category, profileInformation, taskName)

if __name__ == "__main__":            
    proccx = []        
    for task in tasks:
        keywords = tasks[task]["KWs"]
        category = tasks[task]["category"]
        color = tasks[task]["color"]
        size = tasks[task]["size"]
        whichProfile = tasks[task]["profile"]
        profileInformation = gu(whichProfile)

        p = Process(target=go, args=(keywords, color, size, category, profileInformation, task))
        proccx.append(p)
    for p in proccx:
        p.start()

