import time
import json
import threading
import sys
from termcolor import colored
from opensupreme import return_item_ids, add_to_cart, checkout

def get_profile_data(profile_id, profiles_file):
    """
    This function makes sure the profile associated with a task exists prior to starting that task.
    It then returns the profile information if it exists.
    """

    with open(profiles_file) as f:
        profiles = json.load(f)
    index = [profiles.index(profile) for profile in profiles if profile["id"] == profile_id]

    if index:
        index = index[0]
        return profiles[index]
    else:
        return None
      
def run_task(positive_keywords, negative_keywords, category, size, color, profile_data, proxy, delay, task_name, screenlock):
    """
    This function is the target of the threads we make.
    It will keep trying to checkout until it successfully purchases the desired item.
    """

    while True:
        with screenlock:
            print(colored(f"{task_name}: Searching for",  attrs=["bold"]), colored(positive_keywords, "cyan"))

        start_checkout_time = time.time()
        item_id, size_id, style_id = return_item_ids(positive_keywords, negative_keywords, category, size, color, proxy, task_name, screenlock)
        session = add_to_cart(item_id, size_id, style_id, task_name, screenlock)
        if session:
            if checkout(session, profile_data, delay, proxy, task_name, start_checkout_time, screenlock):
                break

def create_threads(tasks_file, profiles_file):
    """
    From tasks.json and profiles.json, assign the neccessary variables needed to checkout for each task.
    Then, create a thread for that task and append it to a list of threads.
    Finally, return the list of threads
    """

    with open(tasks_file) as f:
        tasks = json.load(f)

    threads = []
    screenlock = threading.Lock()

    for task in tasks:
        task_name = task["task_name"]
        positive_keywords = task["pos_kws"]
        negative_keywords = task["neg_kws"]
        delay = task["delay"]

        category = task["category"]
        color = task["color"]
        size = task["size"]
        proxy = task["proxy"]

        profile_id = task["profile_id"]
        profile_data = get_profile_data(profile_id, profiles_file)

        if not profile_data:
            print(colored(f"ERROR: No Associated Profile for '{task_name}'", "red"))
        else:
            t = threading.Thread(target=run_task, args=(
                positive_keywords, negative_keywords, category,
                size, color, profile_data,
                proxy, delay, task_name, screenlock)
            )
            t.daemon = True
            threads.append(t)
    
    return threads

def run_all(tasks_file, profiles_file):
    """
    Create a list which contains threads for each tasks.
    Then, start each thread without joining so they run independently of eachother.
    Run until the task completes or the user supplies input.
    """

    threads = create_threads(tasks_file, profiles_file)
    if threads:
        for t in threads:
            t.start()
        input()






    
