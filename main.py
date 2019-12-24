import time, json
import addRemoveProfiles
import addRemoveTasks
from multiprocessing import Process

from lookForStock import keepLooking as kl
from lookForStock import findStyle as fs
from cartingAndCO import atcCheckout as cartCO
from cartingAndCO import getStatus as gs
from getProfiles import getUsers as gu

with open("tasks.json", "r") as f:
        tasks = json.load(f)
def go(keywords, color, size, category, profileInformation, taskName, proxy, delay):
        start = time.time()
        itemId = kl(keywords, color, size, category, proxy)
        returnedIds = fs(itemId, color, size, category, proxy)


        if returnedIds == None:
            print(f"Error finding style or size for task '{taskName}'\n")
        elif len(returnedIds) == 2:
             styleId = returnedIds[0]
             sizeId = returnedIds[1]

             result = cartCO(itemId, styleId, sizeId, start, profileInformation, proxy, delay)
             print(result[0], result[1])
             
             if "slug" in result[0]:
                 slug = result[0]
                 slug = slug["slug"]
                 print("\n")
                 for _ in range(2):
                     stat = gs(slug, proxy)
                     time.sleep(3.5)
                     print(f"Status for '{taskName}': {stat}")
             else:
                 print(f"Checkout failed for task '{taskName}', restarting\n")
                 time.sleep(1.25)
                 go(keywords, color, size, category, profileInformation, taskName, proxy, delay)
        else:
            print(f"Item sold out for '{taskName}', restarting")
            time.sleep(2)
            go(keywords, color, size, category, profileInformation, taskName, proxy, delay)

def start(jFile):
    if len(jFile) == 0:
        print("Ensure you add tasks and a profile before starting the bot")
        time.sleep(.5)
    proccx = []        
    for task in tasks:
        keywords = tasks[task]["KWs"]
        category = tasks[task]["category"]
        color = tasks[task]["color"]
        size = tasks[task]["size"]
        whichProfile = tasks[task]["profile"]
        proxy = tasks[task]["proxy"]
        delay = tasks[task]["delay"]
        profileInformation = gu(whichProfile)

        p = Process(target=go, args=(keywords, color, size, category, profileInformation, task, proxy, delay))
        proccx.append(p)

    for p in proccx:
        p.start()
    
if __name__ == "__main__":
    with open("tasks.json", "r") as f:
            jFile = json.load(f)
    while True:
        print("1: Profiles")
        print("2: Tasks")
        print("3: Start bot \n")
        a = input("Type here to select: ")
        if a == "1":
            print()
            while True:
                addRemoveProfiles.main()
                break
        elif a == '2':
            print()
            while True:
                addRemoveTasks.main()
                break
        elif a == '3':
            start(jFile)
            break
        else:
            print("Invalid input, try again")
            continue