import re
from bs4 import BeautifulSoup as bs

def get_params(page_content, profile_data, cookie_sub):
    checkout_data = {}
    

    regex = re.compile('[^a-zA-Z]')
    soup = bs(page_content, "html.parser")
    scripts = soup.find_all("script")

    for script in scripts:
        try:
            # Need to find a better way to properly parse
            if len(script.text) > 5000:
                script = script.text
                soup = bs(script, "html.parser")

                select_fields = soup.find_all("select")
                input_fields = soup.find_all("input")

                has_value = []
                no_value = []

                for input_box in input_fields:
                    try:
                        input_box["value"]
                        has_value.append(input_box)
                    except:
                        try:
                            input_box["name"]
                            no_value.append(input_box)
                        except:
                            pass

                for hv in has_value:
                    checkout_data[hv["name"]] = hv["value"]
                    if not hv["value"]:

                        try:
                            placeholder = regex.sub("", hv["placeholder"]).lower().strip()
                            if "cvv" in placeholder:
                                checkout_data[hv["name"]] = profile_data["cvv"]
                            elif "card" in placeholder or "credit" in placeholder:
                                checkout_data[hv["name"]] = profile_data["card_number"]
                            
                        except:
                            checkout_data[hv["name"]] = hv["value"]

                for nv in no_value:
                    try:
                        placeholder = regex.sub("", nv["placeholder"]).lower().strip()
                        name = regex.sub("", nv["name"]).lower().strip()
                        
                        if placeholder == "name" or "name" in nv["name"]:
                            if nv["name"] not in checkout_data:
                                checkout_data[nv["name"]] = profile_data["name"]
                                
                        elif placeholder == "email" or "email" in name or "e-mail" in name or "e-mail" == placeholder:
                            checkout_data[nv["name"]] = profile_data["email"]
                            
                        elif placeholder == "telephone" or placeholder == "tel" or "tel" in name:
                            checkout_data[nv["name"]] = profile_data["tel"]
                            
                        elif placeholder == "address" or placeholder == "billing address" or placeholder == "addr":
                            checkout_data[nv["name"]] = profile_data["address"]
                            
                        elif "apt" in placeholder or "unit" in placeholder:
                            checkout_data[nv["name"]] = profile_data["apt"]
                            
                        elif "zip" in placeholder:
                            checkout_data[nv["name"]] = profile_data["zip"]
                            
                        elif placeholder == "city" or "city" in name:
                            checkout_data[nv["name"]] = profile_data["city"]

                    except:
                        if "cookie" in nv["name"] or "sub" in nv["name"]:
                                checkout_data[nv["name"]] = cookie_sub

                for sf in select_fields:
                    id_ = regex.sub("", sf["id"]).lower().strip()
                    name = regex.sub("", sf["name"]).lower().strip()
                    
                    if  "state" in name or "state" in id_:
                        checkout_data[sf["name"]] = profile_data["state"]
                        
                    elif "country" in name or "country" in id_:
                        checkout_data[sf["name"]] = profile_data["country"]
                        
                    elif "month" in name or "month" in id_:
                        checkout_data[sf["name"]] = profile_data["exp_month"]
                        
                    elif "year" in name or "year" in id_:
                        checkout_data[sf["name"]] = profile_data["exp_year"]

                if check_data(checkout_data, profile_data):
                    return checkout_data
                
        except:
            pass

def check_data(checkout_data, profile_data):
    for key in profile_data:
        if profile_data[key] not in checkout_data.values():

            return False
    return True
