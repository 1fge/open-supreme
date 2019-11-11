import json, time

def main():
    with open("tasks.json", "r") as jFile:
        jsonFile = json.load(jFile)
        
    if len(jsonFile) == 0:
        print("\nCreating a task since none were found")
        addTask(jsonFile)
    else:
        allTasks = []
        for task in jsonFile:
            allTasks.append(task)
        print(f"Current Tasks: {allTasks}\n")
        response = input("Would you like to add, delete, view, or edit tasks?\n'0': Add\n'1': Delete\n'2': View\n'3': Edit\n> ")

        if response.upper() == "add".upper() or response == "0":
            addTask(jsonFile)
        elif response.upper() == "delete".upper() or response == "1":
            deleteTask(jsonFile)
        elif response.upper() == "view".upper() or response == "2":
            viewTask(jsonFile)
        elif response.upper() == "edit".upper() or response == "3":
            editTask(jsonFile)
        else:
            print("Syntax error with choice, restarting\n")
            time.sleep(1.25)
            main()


def addTask(tasksFile):
    with open("profiles.json", "r") as pFile:
        profileFile = json.load(pFile)
    profile = -1            
    taskName = input("Task Name: ")
    keywords = input("Enter all keywords separated by a comma: ")
    keywords = keywords.split(",")
    print(keywords)
    category = input("Category: ")
    color = input("Color: ")
    size = input("Size (N/A for sizeless items): ")
    
    print("\n")
    for a, b in enumerate(profileFile["users"]):
        print(b["name"],",", b["address"], a)
    print("\n")
    
    while int(profile) < 0 or int(profile) > len(profileFile["users"]) - 1:       
        profile = input("Profile Selection (number next to profile name): ")
    profile = "profile" + str(profile)

    print("Adding task\n")
        
    tasksFile[taskName] = {}
    tasksFile[taskName]["KWs"] = keywords
    tasksFile[taskName]["category"] = category
    tasksFile[taskName]["color"] = color
    tasksFile[taskName]["size"] = size
    tasksFile[taskName]["profile"] = profile
    with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)
            time.sleep(2.5)

def deleteTask(tasksFile):
    whichTask = input("Enter the name of the task you wish to delete: ")
    if whichTask not in tasksFile:
        print(f"Could not find task '{whichTask}'\n")
        deleteTask(tasksFile)
    else:
        print(f"Deleting task '{whichTask}'\n")
        del tasksFile[whichTask]

        with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)

        time.sleep(2)

def viewTask(tasksFile):
    whichTask = input("Enter the name of the task you wish to view: ")
    if whichTask not in tasksFile:
        print(f"Could not find task '{whichTask}'\n")
        viewTask(tasksFile)
    else:
        print(f"\nTask Name: {whichTask}")
        print(f"Keywords: {tasksFile[whichTask]['KWs']}")
        print(f"Category: {tasksFile[whichTask]['category']}")
        print(f"Color: {tasksFile[whichTask]['color']}")
        print(f"Size: {tasksFile[whichTask]['size']}")
        print(f"Profile: {tasksFile[whichTask]['profile']}\n")

        time.sleep(2.5)
        
def editTask(tasksFile):
    whichTask = input("Enter the name of the task you wish to edit: ")
    if whichTask not in tasksFile:
        print(f"Could not find task '{whichTask}'\n")
        editTask(tasksFile)
        
    parts = ["task name"]
    for _ in tasksFile[whichTask]:
        parts.append(_)
    whichPart = input(f"\nWhich part of the task would you like to edit?\n({', '.join(parts)}): ")

    if whichPart not in parts:
        print(f"Error, {whichPart} not found in {whichTask}")
        time.sleep(1.5)
        editTask(tasksFile)
    elif whichPart == "task name":
        newName = input(f"Enter new task name for '{whichTask}': ")
        print(f"Name of task '{whichTask}' changed to '{newName}'\n")
        tasksFile[newName] = tasksFile[whichTask]
        del tasksFile[whichTask]

        with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)
        time.sleep(2)
        
    elif whichPart == "KWs":
        print(f"\n{whichTask}'s {whichPart} are currently {tasksFile[whichTask][whichPart]}")
        newKws = input("Enter new keywords with a comma in between each one: ")
        newKws = newKws.split()
        print(f"Changed {whichTask}'s keywords from {tasksFile[whichTask][whichPart]} to {newKws}\n")
        tasksFile[whichTask][whichPart] = newKws
        with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)
        time.sleep(2)
        
    else:
        print(f"\n{whichTask}'s {whichPart} is currently '{tasksFile[whichTask][whichPart]}'")
        newChange = input(f"Enter what you would like to change the {whichPart} to: ")
        print(f"{whichPart} in task {whichTask} changed to {newChange}\n")
        tasksFile[whichTask][whichPart] = newChange

        with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)
        time.sleep(2)
        
while True:
    main()
