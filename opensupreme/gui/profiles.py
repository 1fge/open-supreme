import json
import random
from termcolor import colored


def create_profile_name(profiles):
    """
    Check if any other profiles exist, get user-supplied profile name.
    If other profiles, ensure none are the same.
    as the new profile name, otherwise restart.
    If no other profiles exist, accept any profile name. 
    """

    if profiles:
        profile_names = [profile["profile_name"] for profile in profiles]

        while True:
            profile_name = input("Name for this Profile: ").strip()
            if profile_name not in profile_names:
                return profile_name
            else:
                print("Error, there's already a profile with this name\n")
    else:
        return input("Name for this Profile: ")

def create_profile_id(profiles):
    """
    profile_id is used to identify profiles even if their name changes.
    First check if there are any profiles.
    If there are, get all profile ids.
    Keep generating an id until it isn't in the list of ids.
    If there are no other profiles, return any random int between 0-99998
    """

    if profiles:
        profile_ids = [profile["id"] for profile in profiles]
        while True:
            profile_id = random.randrange(0, 99999)
            if profile_id not in profile_ids:
                return profile_id
    else:
        return random.randrange(0, 99999)

def add_profile(profiles_file):
    """
    Store a copy of the profiles.json file.
    Then, append the following attributes to that copy and write it to profiles.json
    """

    with open(profiles_file) as f:
        profiles = json.load(f)

    profile_name = create_profile_name(profiles)
    profile_id = create_profile_id(profiles)

    profile = {}
    profile["profile_name"] = profile_name
    profile["name"] = input("Cardholder's Name: ").strip()
    profile["email"] = input("Email: ").strip()
    profile["tel"] = input("Telephone xxx-xxx-xxxx: ").strip()
    profile["address"] = input("Address: ").strip()

    profile["apt"] = input("Appt Num (press enter if n/a): ").strip()
    profile["zip"] = input("Zipcode: ").strip()
    profile["city"] = input("City: ").strip()
    profile["state"] = input("State (NY, AZ, CA): ").strip().upper()
    profile["country"] = "USA"

    cn = input("Card Number: ").replace(" ", "").replace("-", "")
    profile["card_number"] = " ".join([cn[i:i+4] for i in range(0, len(cn), 4)])
    profile["exp_month"] = input("Card Expiration Month (01, 02, 10, 11): ").strip()
    profile["exp_year"] = input("Card Expiration Year (2021, 2024): ").strip()
    profile["cvv"] = input("Card CVV: ").strip()
    profile["id"] = profile_id
 
    profiles.append(profile)

    with open(profiles_file, "w") as f:
        json.dump(profiles, f)

def get_profile_with_action(profiles, action):
    """
    Display a list of profile names, 
    ask the user for the profile name they want to do an action on.
    Iterate through list of profiles, check if supplied profile name exists in that list.
    """

    print("Profiles:\n")
    for profile in profiles:
        print(f"{colored(profile['profile_name'], 'yellow')} | {profile['name']} | {profile['address']}")

    profile_for_action = input(f"\nEnter the profile name you want to {action}: ")
    index = [profiles.index(profile) for profile in profiles if profile["profile_name"] == profile_for_action]
    
    return index

def delete_profile(profiles_file):
    """
    Get user's desired profile.
    Delete it if it exists, otherwise tell the user it doesn't.
    """ 

    with open(profiles_file) as f:
        profiles = json.load(f)

    if profiles:
        index = get_profile_with_action(profiles, "delete")
        if index:
            del profiles[index[0]]

            with open(profiles_file, "w") as f:
                json.dump(profiles, f)

            print(colored("Successfully deleted profile", "green"))
        else:
            print(colored(f"No profile with that name", "red"))
    else:
        print(colored("You haven't made a profile yet!", "red"))
    

def nicely_display_profile(profiles, index):
    """
    For a profile at certain index in the profiles list,
    print all its keys and values.
    """
    
    profile = profiles[index]
    for key in profile:
        if key != "id":
            capitalized_key = " ".join(k.capitalize() for k in key.split("_"))
            value_of_key = profile[key]

            print(colored(capitalized_key, 'magenta'), value_of_key)

def view_profile(profiles_file):
    """
    Get user's desired profile.
    Display the contents of that profile if it exists.
    Otherwise, inform user it doesn't.
    """

    with open(profiles_file) as f:
        profiles = json.load(f)
    
    if profiles:
        index = get_profile_with_action(profiles, "view")
        if index:
            index = index[0]
            nicely_display_profile(profiles, index)
        else:
            print(colored(f"No profile with that name", "red"))
    
    else:
        print(colored("You haven't made a profile yet!", "red"))


def get_profile_aspect_to_edit(index, selections, profiles):
    """
    Get the aspect (key for a profile's value) the user wants to change.
    Once they input a valid aspect, return the aspect and associated key.
    """
    
    profile = profiles[index]
    aspects = "\n--- Profile Name, Name, Email\n--- Telephone, Address, Apartment\n--- Zipcode, City, State\n--- Card Number, Exp Month, Exp Year, CVV"
    print(aspects)

    while True:
        aspect = input("\nEnter the aspect you wish to change: ").strip().lower()
        if aspect in selections:
            break

    profile_aspect_key = selections[aspect][0]
    colored_val = colored(repr(profile[profile_aspect_key]), "yellow")
    print(f"Profile's {selections[aspect][1]} is currently {colored_val}\n")

    return aspect, profile_aspect_key

def make_changes_to_profile(profiles, index, selections, aspect, profile_aspect_key):
    """
    Based off of the aspect the user wants to change for their profile,
    give them a description of what the input should be and then make the change.
    """

    if aspect == "card number":
        new_value = input("Card Number: ").replace(" ", "").replace("-", "")
        profiles[index]["card_number"] = " ".join([new_value[i:i+4] for i in range(0, len(new_value), 4)])
    elif aspect == "state":
        profiles[index]["state"] = input("State: (NY, AZ, CA) ").strip().upper()
    elif len(selections[aspect]) == 2:
        profiles[index][profile_aspect_key] = input(f"{selections[aspect][1]}: ").strip()
    else:
        profiles[index][profile_aspect_key] = input(f"{selections[aspect][1]} {selections[aspect][2]}: ").strip()

    return profiles

def edit_profile(profiles_file):
    """
    Make sure there is a profile to edit first.
    Get user's selected profile, ensure that the profile exists. 
    Then, display old value along with any needed information, and get new value.
    """

    with open(profiles_file) as f:
        profiles = json.load(f)

    if profiles:
        index = get_profile_with_action(profiles, "edit")
        if index:
            index = index[0]
            selections = {
                "profile name": ["profile_name", "Profile Name"],
                "name": ["name", "Name"],
                "email": ["email", "Email"],
                "telephone": ["tel", "Telephone", "(xxx-xxx-xxxx)"], 
                "address": ["address", "Address"],
                "apartment": ["apt", "Apartment", "(Press enter if n/a)"], 
                "zipcode": ["zip", "Zipcode"],
                "city": ["city", "City"], 
                "state": ["state", "State"],
                "card number": ["card_number", "Card Number"], 
                "exp month": ["exp_month", "Expiration Month", "(01, 02, 10, 11)"],
                "exp year": ["exp_year", "Expiration Year", "(2021, 2024)"],
                "cvv": ["cvv", "CVV"]
            }
            aspect, profile_aspect_key = get_profile_aspect_to_edit(index, selections, profiles)
            profiles = make_changes_to_profile(profiles, index, selections, aspect, profile_aspect_key)

            with open(profiles_file, "w") as f:
                json.dump(profiles, f)
            print(colored("Successfully Edited Profile!", "green"))
        else:
            print(colored(f"No profile with that name", "red"))
    else:
        print(colored("You haven't made a profile yet!", "red"))
