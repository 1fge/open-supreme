import os
import json
import colorama
from termcolor import colored
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
                    selection = item

                    return selection

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
    else:
        mainmenu()

    if selection != 4:
        profiles(profiles_path)

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
    else:
        mainmenu()

    if selection != 4:
        tasks(tasks_path, profiles_path)

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
    else:
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
        tasks = json.load(f)
    if tasks:
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
if __name__ == "__main__":            
    mainmenu()
