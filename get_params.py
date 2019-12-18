from bs4 import BeautifulSoup as bs
import re, time

def get_params(myProfile, checkout_page, cookSub):
    
    regex = re.compile('[^a-zA-Z]') 
    soup = bs(checkout_page, "html.parser")
    all_scripts = soup.find_all("script")

    def find_params_script(all_scripts):
        coData = {}
        for script in all_scripts:
            try:
                script = script.text
                soup = bs(script, "html.parser")
                select_fields = soup.find_all("select")
                input_fields = soup.find_all("input")

                has_value = []
                no_value = []

                for input_box in input_fields:
                    try:
                        value_check = input_box["value"]
                        has_value.append(input_box)
                    except:
                        try:
                            cause_error = input_box["name"]
                            no_value.append(input_box)
                        except:
                            pass
                       
                for hv in has_value:
                    coData[hv["name"]] = hv["value"]
                    if hv["value"] == "":
                        try:
                            placeholder = regex.sub("", hv["placeholder"]).lower().strip()
                            if "cvv" in placeholder or "cvv" == placeholder:
                                coData[hv["name"]] = myProfile["userCvv"]
                            elif "card" in placeholder or "credit" in placeholder:
                                coData[hv["name"]] = myProfile["userCardNumber"]
                            
                        except:
                            coData[hv["name"]] = hv["value"]

                for nv in no_value:
                    try:
                        placeholder = regex.sub("", nv["placeholder"]).lower().strip()
                        name = regex.sub("", nv["name"]).lower().strip()
                        
                        if placeholder == "name" or "name" in nv["name"]:
                            if nv["name"] not in coData:
                                coData[nv["name"]] = myProfile["userName"]
                                
                        elif placeholder == "email" or "email" in name or "e-mail" in name or "e-mail" == placeholder:
                            coData[nv["name"]] = myProfile["userEmail"]
                            
                        elif placeholder == "telephone" or placeholder == "tel" or "tel" in placeholder or "tel" in name:
                            coData[nv["name"]] = myProfile["userTel"]
                            
                        elif placeholder == "address" or placeholder == "billing address" or placeholder == "addr":
                            coData[nv["name"]] = myProfile["userAddress"]
                            
                        elif placeholder == "apt, unit, etc" or "apt" in placeholder or "unit" in placeholder:
                            coData[nv["name"]] = myProfile["userApt"]
                            
                        elif placeholder == "zip" or placeholder == "billing zip" or "zip" in placeholder:
                            coData[nv["name"]] = myProfile["userZip"]
                            
                        elif placeholder == "city" or "city" in name:
                            coData[nv["name"]] = myProfile["userCity"]
                    except:
                        if "cookie" in nv["name"] or "sub" in nv["name"]:
                             coData[nv["name"]] = cookSub

                for sf in select_fields:
                    id_ = regex.sub("", sf["id"]).lower().strip()
                    name = regex.sub("", sf["name"]).lower().strip()
                    
                    if  "state" in name or "state" in id_:
                        coData[sf["name"]] = myProfile["userState"]
                        
                    elif "country" in name or "country" in id_:
                        coData[sf["name"]] = myProfile["userCountry"]
                        
                    elif "month" in name or "month" in id_:
                        coData[sf["name"]] = myProfile["userExpMonth"]
                        
                    elif "year" in name or "year" in id_:
                        coData[sf["name"]] = myProfile["userExpYear"]

                if check_data(coData):
                    return coData
                
            except:
                pass
        

    def check_data(coData):
        for x in myProfile:
            x = myProfile[x]
            if x not in coData.values():
                return False
        return True
    return find_params_script(all_scripts)

