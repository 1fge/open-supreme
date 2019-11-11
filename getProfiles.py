import json

profilesFile = "profiles.json"
users = {}

def getUsers(whichProfile):
    with open(profilesFile, "r") as pf:
        data = json.load(pf)

        for i in range(len(data["users"])):
            curProf = "profile{}".format(i)
            users[curProf] = {}
            
            userName = data["users"][i]["name"]
            users[curProf]["userName"] = userName
            userEmail = data["users"][i]["email"]
            users[curProf]["userEmail"] = userEmail
            
            userTel = data["users"][i]["tel"]
            users[curProf]["userTel"] = userTel
            userAddress = data["users"][i]["address"]
            users[curProf]["userAddress"] = userAddress
                               
            userApt = data["users"][i]["apt"]
            users[curProf]["userApt"] = userApt
            userZip = data["users"][i]["zip"]
            users[curProf]["userZip"] = userZip
            
            userCity = data["users"][i]["city"]
            users[curProf]["userCity"] = userCity
            userState = data["users"][i]["state"]
            users[curProf]["userState"] = userState
            
            userCountry = data["users"][i]["country"]
            users[curProf]["userCountry"] = userCountry
            userCardNumber = data["users"][i]["cardNumber"]
            users[curProf]["userCardNumber"] = userCardNumber
            userExpMonth = data["users"][i]["expMonth"]
            users[curProf]["userExpMonth"] = userExpMonth
            
            userExpYear = data["users"][i]["expYear"]
            users[curProf]["userExpYear"] = userExpYear 
            userCvv = data["users"][i]["cvv"]
            users[curProf]["userCvv"] = userCvv
            
            
    profInfo = {}
    profiles = users

    userName = profiles[whichProfile]["userName"]
    userEmail = profiles[whichProfile]["userEmail"]
    userTel = profiles[whichProfile]["userTel"]
    userAddress = profiles[whichProfile]["userAddress"]
    userApt = profiles[whichProfile]["userApt"]
    userZip = profiles[whichProfile]["userZip"]
    userCity = profiles[whichProfile]["userCity"]
    userState = profiles[whichProfile]["userState"]
    userCountry = profiles[whichProfile]["userCountry"]
    userCardNumber = profiles[whichProfile]["userCardNumber"]
    userExpMonth = profiles[whichProfile]["userExpMonth"]
    userExpYear = profiles[whichProfile]["userExpYear"]
    userCvv = profiles[whichProfile]["userCvv"]

    profInfo["userName"] = userName
    profInfo["userEmail"] = userEmail
    profInfo["userTel"] = userTel
    profInfo["userAddress"] = userAddress
    profInfo["userApt"] = userApt
    profInfo["userZip"] = userZip
    profInfo["userCity"] = userCity
    profInfo["userState"] = userState
    profInfo["userCountry"] = userCountry
    profInfo["userCardNumber"] = userCardNumber
    profInfo["userExpMonth"] = userExpMonth
    profInfo["userExpYear"] = userExpYear
    profInfo["userCvv"] = userCvv

    return profInfo
