import json, time

def main():
    with open("profiles.json", "r") as jFile:
        jsonFile = json.load(jFile)
        
    if len(jsonFile["users"]) == 0:
        print("\nCreating a profile since none were found")
        addProf(jsonFile)
    else:
        allProfs = [(prof["name"], prof["address"]) for prof in jsonFile["users"]]
        print("Current Profiles: ")
        
        for i in range(len(allProfs)):
            print(allProfs[i], i)
        print("\n")
        
        response = input("Would you like to add, delete, view, or edit profiles?\n'0': Add\n'1': Delete\n'2': View\n'3': Edit\n> ")

        if response.upper() == "add".upper() or response == "0":
            addProf(jsonFile)
        elif response.upper() == "delete".upper() or response == "1":
            deleteProf(jsonFile, allProfs)
        elif response.upper() == "view".upper() or response == "2":
            viewProf(jsonFile)
        elif response.upper() == "edit".upper() or response == "3":
            editProf(jsonFile, allProfs)
        else:
            print("Syntax error with choice, restarting\n")
            time.sleep(1.25)
            main()


def addProf(profFile):
    curDict = {}
    curDict["name"] = input("Cardholder's Name: ")
    curDict["email"] = input("Email: ")
    curDict["tel"] = input("Telephone (xxx-xxx-xxxx): ")
    curDict["address"] = input("Address: ")
    curDict["apt"] = input("Appt Num (press enter if n/a): ")
    curDict["zip"] = input("Zipcode: ")
    curDict["city"] = input("City: ")
    curDict["state"] = input("State (NY, AZ, CA): ")
    curDict["country"] = "USA"
    curDict["cardNumber"] = input("Card Number (Put spaces every 4 digits): ")
    curDict["expMonth"] = input("Card Expiration Month (01, 02, 10, 11): ")
    curDict["expYear"] = input("Card Expiration Year: ")
    curDict["cvv"] = input("Card CVV: ")
    print("\nAppending to Profiles")

    profFile["users"].append(curDict)
    with open("profiles.json", "w") as f:
        json.dump(profFile, f)
        
    time.sleep(1.75)
def deleteProf(profFile, allProfs):
    profSelection = input("Enter the number of the profile you want to delete: ")
    try:
        profSelection = int(profSelection)
        while profSelection < 0 or profSelection > len(allProfs)- 1:
            profSelection = int(input("Error, enter the number next to the profile you want to delete: "))
        print(f"Deleting profile {allProfs[profSelection]}\n")
        del profFile["users"][profSelection]
        with open("profiles.json", "w") as f:
            json.dump(profFile, f)
                       
    except:
        print("Error with selection")
        time.sleep(1.75)
        deleteProf(profFile, allProfs)
               
    time.sleep(1.75)
def viewProf(profFile):
    profSelection = input("Enter the number of the profile you want to view: ")
    try:
        profSelection = int(profSelection)
        print("\n")
        print(f"Name: {profFile['users'][profSelection]['name']}")
        print(f"Email: {profFile['users'][profSelection]['email']}")
        print(f"Telephone: {profFile['users'][profSelection]['tel']}")
        print(f"Address: {profFile['users'][profSelection]['address']}")
        print(f"Apartment: {profFile['users'][profSelection]['apt']}")
        print(f"Zip Code: {profFile['users'][profSelection]['zip']}")
        print(f"City: {profFile['users'][profSelection]['city']}")
        print(f"State: {profFile['users'][profSelection]['state']}")
        print(f"Card Number: {profFile['users'][profSelection]['cardNumber']}")
        print(f"Expiration Month: {profFile['users'][profSelection]['expMonth']}")
        print(f"Expiration Year: {profFile['users'][profSelection]['expYear']}")
        print(f"CVV: {profFile['users'][profSelection]['cvv']}\n")
        time.sleep(1.75)
    except:
        print("Error, enter the number next to the desired profile")
        time.sleep(1.0)
        viewProf(profFile)
        
def editProf(profFile, allProfs):
    whichProf = input("Enter the number of the profile you want to edit: ")
    try:
        whichProf = int(whichProf)
        print(f"Enter aspect of {allProfs[whichProf]} you want to edit \n(CASE SENSITIVE)\n")

        aspects = ["name", "email", "tel", "address", "apt", "zip", "city", "state", "country", "cardNumber", "expMonth", "expYear", "cvv"]
        whichAspect = None
        while whichAspect not in aspects:
            whichAspect = input(f"Aspects: \n{aspects}: ")

        print(f'\n"{whichAspect}" is currently {profFile["users"][whichProf][whichAspect]}')
        changeTo = input(f"Enter new {whichAspect}: ")
        print("Updating Profile\n")
        profFile["users"][whichProf][whichAspect] = changeTo

        with open("profiles.json", "w") as f:
            json.dump(profFile, f)
            
    except Exception as e:
        print(e)
        print("Error with selection")
        time.sleep(1.75)
        editProf(profFile, allProfs)
    time.sleep(1.75)

while True:
    main()
