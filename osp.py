import os
import json
import logging
import colorama
import threading
from termcolor import colored
from harvester import Harvester
from opensupreme import run_all
from opensupreme.gui import (add_profile, delete_profile, view_profile, 
    edit_profile, add_task, delete_task, view_task, edit_task)

def select_choice(selections):
    """
    Keep asking a user for a selection until it is valid
    """

    while True:
        user_choice = input("> ")
        for item in selections:
            for selection_tag in selections[item]:
                if user_choice.lower().strip() == selection_tag:
                    return item

def profiles(profiles_path):
    """
    Based off of the user's selection, either create, delete, 
    view, or edit a profile. 
    Also offer the option to return to the main menu.
    """
    
    print(colored("\nProfiles", "yellow"))
    print("0: Add\n1: Delete\n2: View\n3: Edit\n4: Main Menu\n")

    selections = {
        0: ["0", "add"],
        1: ["1", "delete"],
        2: ["2", "view"],
        3: ["3", "edit"],
        4: ["4", "main menu", "mm"]
    }

    selection = select_choice(selections)
    
    if selection == 0:
        add_profile(profiles_path)
    elif selection == 1:
        delete_profile(profiles_path)
    elif selection == 2:
        view_profile(profiles_path)
    elif selection == 3:
        edit_profile(profiles_path)
    elif selection == 4:
        mainmenu()

    selection != 4 and profiles(profiles_path) # use short-circuit evaluation to run profiles function if selection not mainmenu

def tasks(tasks_path, profiles_path):
    """
    Based off of the user's selection, either create, delete, 
    view, or edit a task. 
    Also offer the option to return to the main menu.
    """

    print(colored("\nTasks", "yellow"))
    print("0: Add\n1: Delete\n2: View\n3: Edit\n4: Main Menu\n")

    selections = {
        0: ["0", "add"],
        1: ["1", "delete"],
        2: ["2", "view"],
        3: ["3", "edit"],
        4: ["4", "main menu", "mm"]
    }

    selection = select_choice(selections)

    if selection == 0:
        add_task(tasks_path, profiles_path)
    elif selection == 1:
        delete_task(tasks_path, profiles_path)
    elif selection == 2:
        view_task(tasks_path, profiles_path)
    elif selection == 3:
        edit_task(tasks_path, profiles_path)
    elif selection == 4:
        mainmenu()

    selection != 4 and tasks(tasks_path, profiles_path)

def runbot(tasks_file, profiles_file):
    print(colored("Open Supreme\n", "yellow"))
    print("run: Start Tasks\n1: Main Menu\n")

    selections = {
        "run": ["run", "start tasks"],
        "mainmenu": ["1", "main menu"]
    }

    selection = select_choice(selections)

    if selection == "run":
        run_all(tasks_file, profiles_file)
    mainmenu()

def profiles_exist(profiles_file):
    """
    Open profiles.json, check that the user has made profiles
    """

    with open(profiles_file) as f:
        profiles = json.load(f)
    if profiles:
        return True

def tasks_exist(tasks_file):
    """
    Check whether the user has any tasks made prior to starting the bot.
    """

    with open(tasks_file) as f:
        if json.load(f):
            return True

def mainmenu():
    """
    This is where the main function where users can access task options,
    profile options, or start all tasks.
    """

    colorama.init()
    tasks_path = os.path.abspath("data//tasks.json")
    profiles_path = os.path.abspath("data//profiles.json")

    print(colored("\nMain Menu", "yellow"))
    print("0: Profiles\n1: Tasks\n2: Open-Supreme\n")

    selections = {
        0: ["0", "profiles"],
        1: ["1", "tasks"],
        2: ["2", "open-supreme", "os"]
    }

    selection = select_choice(selections)

    if selection == 0:
        profiles(profiles_path)
    elif selection == 1:
        if profiles_exist(profiles_path):
            tasks(tasks_path, profiles_path)
        else:
            print(colored("You must make a profile first!", "red"))
            mainmenu()
    else:
        if tasks_exist(tasks_path):
            runbot(tasks_path, profiles_path)
        else:
            print(colored("You must make a task first!", "red"))
            mainmenu()

def start_captcha_server():
    logging.getLogger('harvester').setLevel(logging.CRITICAL)
    harvester = Harvester()

    tokens = harvester.intercept_recaptcha_v2(
        domain='www.supremenewyork.com',
        sitekey='6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz'
    )

    server_thread = threading.Thread(target=harvester.serve, daemon=True)
    server_thread.start()
    harvester.launch_browser()

if __name__ == "__main__":
    start_captcha_server()
    mainmenu()
