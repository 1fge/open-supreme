import time
import json
import threading
from opensupreme import find_id, atc, checkout

with open("tasks.json") as f:
    tasks = json.load(f)

def run_task(kws, cat, size, color, profile_data, proxy, delay):
    while True:
        ids = find_id(kws, cat, size, color, proxy)
        session = atc(ids[0], ids[1], ids[2])
        if checkout(session, profile_data, delay, proxy):
            break
        

profile_data = {
    "name": "Example Name",
    "email": "exampleemail@mail.com",
    "tel": "123-456-7891",
    "address": "123 lane road",
    "apt": "",
    "zip": "10010",
    "city": "Manhattan",
    "state": "NY",
    "country": "USA",
    "card_number": "0000 0000 0000 0000",
    "exp_month": "04",
    "exp_year": "2023",
    "cvv": "123"
}

tx = []
for task in tasks:
    vals = tasks[task]
    p_kws = tuple(vals["pos_kws"])
    n_kws = tuple(vals["neg_kws"])
    kws = (p_kws, n_kws)
    
    cat = vals["category"]
    size = vals["size"]
    color = vals["color"]
    proxy = vals["proxy"]
    delay = vals["delay"]

    t = threading.Thread(target=run_task, args=(kws, cat, size, color, profile_data, proxy, delay))
    tx.append(t)

for t in tx:
    t.start()





    
