import json
from termcolor import colored

def create_task_name(tasks):
    """
    Have user create unique task name.
    """

    if tasks:
        task_names = [task["task_name"] for task in tasks]
        while True:
            task_name = input("Name for this task: ").strip()
            if task_name not in task_names:
                return task_name
            else:
                print(colored("A task with that name already exists!", "red"))
    else:
        return input("Name for this task: ").strip()

def set_checkout_delay():
    """
    Have user input valid float for a checkout delay
    """

    while True:
        delay = input("Checkout Delay (seconds): ").strip()
        try:
            delay = float(delay)
            return delay
        except:
            print(colored("Invalid Delay", "red"))
 
def assign_profile(profiles_file):
    """
    Assign a profile to a task by the profile's id.
    This ensures that if the profile's name changes, 
    the profile will still be associated with the task.
    """

    with open(profiles_file) as f:
        profiles = json.load(f)
    
    for profile in profiles:
        print(f"{colored(profile['profile_name'], 'yellow')} | {profile['name']} | {profile['address']}")

    while True:
        profile_to_edit = input("\nEnter the profile name you want to select: ")
        index = [profiles.index(profile) for profile in profiles if profile["profile_name"] == profile_to_edit]

        if index:
            index = index[0]
            profile_id = profiles[index]["id"]
            return profile_id

def add_task(tasks_file, profiles_file):
    """
    Get all necessary information required to successfully checkout from the user.
    """

    with open(tasks_file) as f:
        tasks = json.load(f)

    task = {}
    task["task_name"] = create_task_name(tasks)
    positive_keywords = input("Enter all positive keywords separated by a comma: ")
    task["pos_kws"] = [keyword.strip() for keyword in positive_keywords.split(",")]
    negative_keywords = input("Enter all negative keywords separated by a comma (press enter if you don't have any) ").strip()

    if negative_keywords:
        task["neg_kws"] = [keyword.strip() for keyword in negative_keywords.split(",")]
    else:
        task["neg_kws"] = None

    task["delay"] = set_checkout_delay()
    task["category"] = input("Category: ").strip()
    task["color"] = input("Color: ").strip()

    size = input("Size (press enter if it's one-size): ").strip()
    if not size:
        size = "N/A"

    task["size"] = size
    task["proxy"] = input("Proxy & Port ex. 1.1.1.1:111 (press enter if you don't have any): ").strip()
    task["profile_id"] = assign_profile(profiles_file)

    tasks.append(task)

    with open(tasks_file, "w") as f:
        json.dump(tasks, f)


def lookup_profile(profile_id, profiles_file):
    """
    Lookup a profile name by it's id for a given task.
    """
    
    with open(profiles_file) as f:
        profiles = json.load(f)

    index = [profiles.index(profile) for profile in profiles if profile["id"] == profile_id]
    if index:
        index = index[0]
        profile_name = profiles[index]["profile_name"]

        return profile_name
    else:
        return "ASSOCIATED PROFILE DELETED"
          
def display_tasks(tasks, profiles_file):
    """
    For each task, display its name, 
    the name of the profile associated with it,
    and its positive keywords.
    """

    print("Tasks:\n")
    for task in tasks:
        task_name = task["task_name"]
        profile_name = lookup_profile(task["profile_id"], profiles_file)
        print(f"{colored(task_name, 'yellow')} | {colored(profile_name, 'cyan')} ")

def delete_task(tasks_file, profiles_file):
    """
    Delete a task from tasks.json based off its name.
    """

    with open(tasks_file) as f:
        tasks = json.load(f)

    if tasks:
        display_tasks(tasks, profiles_file)
        task_to_delete = input("\nEnter the task name you want to delete: ")
        index = [tasks.index(task) for task in tasks if task["task_name"] == task_to_delete]

        if index:
            index = index[0]
            del tasks[index]

            with open(tasks_file, "w") as f:
                json.dump(tasks, f)

            print(colored(f"Successfully deleted {task_to_delete}", "green"))
        else:
            print(colored(f"No task named '{task_to_delete}'", "red"))
    else:
        print(colored("You haven't made a task yet!", "red"))

def display_task_attributes(task, profiles_file):
    """
    For a given task, display all of the keys and values associated with it.
    """

    profile_id = task["profile_id"]
    profile_name = lookup_profile(profile_id, profiles_file)
    print(colored("\nProfile ", "magenta"), profile_name)

    for key in task:
        if "id" not in key:
            capitalized_key = " ".join(k.capitalize() for k in key.split("_"))
            value_of_key = task[key]

            print(colored(capitalized_key, 'magenta'), value_of_key)
                
def view_task(tasks_file, profiles_file):
    """
    Find the task the user wants to view,
    use display_task_attributes to display all of its attributes.
    """

    with open(tasks_file) as f:
        tasks = json.load(f)
    if tasks:
        display_tasks(tasks, profiles_file)
        task_to_view = input("\nEnter the task name you want to view: ")
        index = [tasks.index(task) for task in tasks if task["task_name"] == task_to_view]

        if index:
            index = index[0]
            task = tasks[index]
            display_task_attributes(task, profiles_file)
        else:
            print(colored(f"No task named '{task_to_view}'", "red"))
    else:
        print(colored("You haven't made a task yet!", "red"))


def get_task_aspect_to_edit(index, selections, tasks, profiles_file):
    """
    For a certain task, return the aspect and its key the user wants to edit.
    """

    task = tasks[index]
    aspects = "\n--- Task Name, Positive Keywords, Negative Keywords\n--- Delay, Category, Color\n--- Size, Proxy, Profile\n"
    print(aspects)

    while True:
        aspect = input("\nEnter the aspect you wish to change: ").strip().lower()
        if aspect in selections:
            break
    task_aspect_key = selections[aspect][0]

    if aspect != "profile":
        colored_val = colored(repr(task[task_aspect_key]), "yellow") 
        print(f"Tasks's {selections[aspect][1]} is currently {colored_val}\n")
    else:
        profile_id = task["profile_id"]
        profile_name = colored(repr(lookup_profile(profile_id, profiles_file)), "yellow")
        print(f"Tasks's Profile is currently {profile_name}")

    return aspect, task_aspect_key

def make_changes_to_task(tasks, index, selections, aspect, task_aspect_key, profiles_file):
    """
    As certain task aspects have specific functions and prompts,
    get the new value based off the aspect.
    """

    if aspect == "delay":
        tasks[index]["delay"] = set_checkout_delay()

    elif aspect == "task name":
        tasks[index]["task_name"] = create_task_name(tasks)

    elif aspect == "positive keywords":
        positive_keywords = input("Enter all positive keywords separated by a comma: ")
        tasks[index]["pos_kws"] = [keyword.strip() for keyword in positive_keywords.split(",")]

    elif aspect == "negative keywords":
        negative_keywords = input("Enter all negative keywords separated by a comma (press enter if you don't have any) ").strip()
        if negative_keywords:
            tasks[index]["neg_kws"] = [keyword.strip() for keyword in negative_keywords.split(",")]
        else:
            tasks[index]["neg_kws"] = None

    elif aspect == "profile":
        tasks[index]["profile_id"] = assign_profile(profiles_file)

    elif len(selections[aspect]) == 2:
        tasks[index][task_aspect_key] = input(f"{selections[aspect][1]}: ").strip()

    else:
        tasks[index][task_aspect_key] = input(f"{selections[aspect][1]} {selections[aspect][2]}: ").strip()

    return tasks

def edit_task(tasks_file, profiles_file):
    """
    Get the edited tasks list, and write over the older one.
    """

    with open(tasks_file) as f:
        tasks = json.load(f)

    if tasks:
        display_tasks(tasks, profiles_file)

        task_to_edit = input("\nEnter the task name you want to edit: ")
        index = [tasks.index(task) for task in tasks if task["task_name"] == task_to_edit]

        if index:
            index = index[0]
            selections = {
                "task name": ["task_name", "Task Name"],
                "positive keywords": ["pos_kws", "Positive Keywords"],
                "negative keywords": ["neg_kws", "Negative Keywords"],
                "category": ["category", "Category"],
                "color": ["color", "Color"],
                "delay": ["delay", "Delay"],
                "size": ["size", "Size"],
                "proxy": ["proxy", "Proxy", "Proxy & Port ex. 1.1.1.1:111 (press enter if you don't have any)"],
                "profile": ["profile_id", "Profile Name"]
            }

            aspect, task_aspect_key = get_task_aspect_to_edit(index, selections, tasks, profiles_file)
            tasks = make_changes_to_task(tasks, index, selections, aspect, task_aspect_key, profiles_file)

            with open(tasks_file, "w") as f:
                json.dump(tasks, f)
            print(colored("Successfully Edited Task!", "green"))
        else:
            print(colored(f"No profile with that name", "red"))

    else:
        print(colored("You haven't made a task yet!", "red"))

    