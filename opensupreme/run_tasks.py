import sys
import time
import json
import requests
import threading
from termcolor import colored
from opensupreme import return_item_ids, add_to_cart, checkout

class SignaledSession(requests.Session):
    """Custom requests Session class which which checks if the threading.Event is set before each request"""
    def __init__(self):
        super().__init__()

    def get(self, url, **kwargs):
        if self.event.is_set():
            sys.exit()
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        if self.event.is_set():
            sys.exit()
        return self.request('POST', url, **kwargs)

class Task(threading.Thread):
    """Class for each 'task' we wish to run, allows for easily stopping / starting task with threading.Event"""
    def __init__(self, positive_keywords, negative_keywords, category, size, color, profile_data, proxy, delay, task_name, screenlock):
        threading.Thread.__init__(self)

        self.positive_keywords = positive_keywords
        self.negative_keywords = negative_keywords
        self.category = category
        self.size = size
        self.color = color
        self.profile_data = profile_data
        self.proxy = proxy
        self.delay = delay
        self.task_name = task_name
        self.screenlock = screenlock

        self.event = threading.Event()
        self.session = SignaledSession()
        self.session.event = self.event # pass the threading Event to our custom Session so we can easily check if set

    def run(self):
        set_session_proxy(self.session, self.proxy)
        run_task(
            self.session,
            self.positive_keywords,
            self.negative_keywords,
            self.category,
            self.size,
            self.color,
            self.profile_data,
            self.delay,
            self.task_name,
            self.screenlock
        )

    def stop(self):
        self.event.set()

def set_session_proxy(session, proxy):
    """ Set the proxy to be used by the session

    Args:
        session (requests.Session): Session object used in all requests
        proxy (str): Proxy with which to use with session object
    """
    proxy = proxy.strip().lower()
    proxies = {}

    if proxy and proxy.count(":") > 1:
        ip, port, user, password = proxy.split(":")
        proxies = {
            "http" : f"http://{user}:{password}@{ip}:{port}",
            "https": f"https://{user}:{password}@{ip}:{port}"
        }
    elif proxy:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
    session.proxies.update(proxies)

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

def run_task(session, positive_keywords, negative_keywords, category, size, color, profile_data, delay, task_name, screenlock):
    """
    This function is the target of the threads we make.
    It will keep trying to checkout until it successfully purchases the desired item.
    """
    while True:
        with screenlock:
            print(colored(f"{task_name}: Searching for",  attrs=["bold"]), colored(positive_keywords, "cyan"))

        start_checkout_time = time.time()
        item_id, size_id, style_id, atc_chk = return_item_ids(session, positive_keywords, negative_keywords, category, size, color, task_name, screenlock)
        session, successful_atc = add_to_cart(session, item_id, size_id, style_id, atc_chk, task_name, screenlock)

        if successful_atc and checkout(session, profile_data, delay, task_name, start_checkout_time, screenlock):
            break

def create_threads(tasks_file, profiles_file):
    with open(tasks_file) as f:
        tasks = json.load(f)

    task_threads = []
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
            task_thread = Task(positive_keywords, negative_keywords, category, size, color, profile_data, proxy, delay, task_name, screenlock)
            task_threads.append(task_thread)
    return task_threads


def run_all(tasks_file, profiles_file):
    """
    Create a list which contains threads for each tasks.
    Then, start each thread so they can run independent of eachother.
    Run until the task completes or the user supplies input.
    """

    threads = create_threads(tasks_file, profiles_file)
    if threads:
        for t in threads:
            t.start()

    input() # Allow user to stop all tasks by entering any combination of keys
    for t in threads:
        t.stop()
    for t in threads: # t.join() # Wait for thread to terminate before handing back control
        t.join()