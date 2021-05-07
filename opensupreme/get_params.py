import re
from bs4 import BeautifulSoup as bs


def sanitize_value(value):
    """Remove any whitespace and non-alphabetical characters"""
    regex = re.compile('[^a-zA-Z]')
    return regex.sub("", value).lower().strip()


def parse_input_fields(input_fields):
    """Separate the input fields into inputs which have `value` and `name` attrs

    Args:
        input_fields (bs4.element.ResultSet): Collection of input values

    Returns:
        [list, list]: Input fields separated by if they `value` and `name` attrs
    """

    custom_values = []
    default_values = []

    for field in input_fields:
        if field.get("value") is not None:
            custom_values.append(field)
        elif field.get("name") is not None:
            default_values.append(field)
    return custom_values, default_values


def assign_custom_values(checkout_data, profile_data, custom_values):
    """Parse default values from supreme's page (pertaining to billing information)

    Args:
        checkout_data (dict): Shipping and billing information which will be posted to checkout
        profile_data (dict): Billing and shipping information for a specific task
        custom_values (list): List of html elements to parse

    Returns:
        dict: checkout_data with appended values
    """

    for value in custom_values:
        if value["name"] not in checkout_data:
            checkout_data[value["name"]] = value["value"]

        if not value["value"]:
            placeholder = value.get("placeholder")
            if placeholder is None:
                checkout_data[value["name"]] = value["value"]
                continue

            placeholder = sanitize_value(placeholder)
            value_name = value["name"]
            if "cvv" in placeholder:
                checkout_data[value_name] = profile_data["cvv"]
            elif "card" in placeholder or "credit" in placeholder:
                checkout_data[value_name] = profile_data["card_number"]
        else:
            name = sanitize_value(value.get("name", ""))
            input_value = sanitize_value(value.get("value", ""))

            if "credit" in name and "type" in name and "credit" in input_value:
                checkout_data[value.get("name")] = value.get("value")
            elif "terms" in name or "terms" in sanitize_value(value.get("id", "")) and input_value != "0":
                checkout_data[value.get("name")] = value.get("value")
    return checkout_data


def get_default_values(checkout_data, profile_data, default_values, cookie_sub):
    """Parse default values from supreme's page (pertaining to shipping information)

    Args:
        checkout_data (dict): Shipping and billing information which will be posted to checkout
        profile_data (dict): Billing and shipping information for a specific task
        default_values (list): List of html elements to parse

    Returns:
        dict: checkout_data with appended values
    """

    for default_value in default_values:
        placeholder = default_value.get("placeholder")
        name = default_value.get("name")

        if placeholder is None or name is None: # only do following operations of placeholder and name are not None
            if name is not None and("cookie" in name or "sub" in name):
                checkout_data[default_value["name"]] = cookie_sub
            continue

        placeholder = sanitize_value(placeholder)
        name = sanitize_value(name)

        if placeholder == "name" or "name" in default_value["name"]:
            if default_value.get("name") not in checkout_data:
                if default_value.get("style") is None:
                    checkout_data[default_value["name"]] = profile_data["name"]
                else:
                    checkout_data[default_value["name"]] = ""

        elif placeholder == "email" or placeholder == "e-mail" or "email" in name or "e-mail" in name:
            checkout_data[default_value["name"]] = profile_data["email"]

        elif placeholder == "telephone" or placeholder == "tel" or "tel" in name:
            checkout_data[default_value["name"]] = profile_data["tel"]

        elif placeholder == "address" or placeholder == "billing address" or placeholder == "addr":
            checkout_data[default_value["name"]] = profile_data["address"]

        elif "apt" in placeholder or "unit" in placeholder:
            checkout_data[default_value["name"]] = profile_data["apt"]

        elif "zip" in placeholder:
            checkout_data[default_value["name"]] = profile_data["zip"]

        elif placeholder == "city" or "city" in name:
            checkout_data[default_value["name"]] = profile_data["city"]

    return checkout_data


def get_select_field_values(checkout_data, profile_data, select_fields):
    """For each <select> element, dynamically determine the proper field name for the checkout data

    Args:
        checkout_data (dict): Shipping and billing information which will be posted to checkout
        profile_data (dict): Billing and shipping information for a specific task
        select_fields (bs4.element.ResultSet): Collection of select elements to parse

    Returns:
        dict: checkout_data with appended values
    """

    for select_field in select_fields:
        element_id = select_field.get("id")
        name = select_field.get("name")
        if select_field is None or name is None:
            continue

        element_id = sanitize_value(element_id)
        name = sanitize_value(name)

        if "state" in name or "state" in element_id:
            checkout_data[select_field["name"]] = profile_data["state"]

        elif "country" in name or "country" in element_id:
            checkout_data[select_field["name"]] = profile_data["country"]

        elif "month" in name or "month" in element_id:
            checkout_data[select_field["name"]] = profile_data["exp_month"]

        elif "year" in name or "year" in element_id:
            checkout_data[select_field["name"]] = profile_data["exp_year"]

    return checkout_data


def check_data(checkout_data, profile_data):
    """Ensure that each value from profile_data is within checkout_data

    Args:
        checkout_data (dict): Shipping and billing information which will be posted to checkout
        profile_data (dict): Billing and shipping information for a specific task

    Returns:
        bool: True for valid data, False otherwise
    """

    for key in profile_data:
        if key != "id" and key != "profile_name":
            if profile_data[key] not in checkout_data.values():
                return False
    return True


def get_params(page_content, profile_data, cookie_sub):
    """Parse checkout parameters from www.supremenewyork.com/mobile/

    Args:
        page_content (str): Response from www.supremenewyork.com/mobile/
        profile_data (dict): Billing and shipping information for a specific task
        cookie_sub (str): Cookie from current session which must be included in checkout data

    Returns:
        [requests.Session/None]: requests.Session if checkout data is valid, None otherwise
    """

    soup = bs(page_content, "html.parser")
    scripts = soup.find_all("script")

    for script in scripts:
        try:
            checkout_data = {}
            script = script.text
            soup = bs(script, "html.parser")

            select_fields = soup.find_all("select")
            input_fields = soup.find_all("input")
            custom_values, default_values = parse_input_fields(input_fields)

            checkout_data = assign_custom_values(checkout_data, profile_data, custom_values)
            checkout_data = get_default_values(checkout_data, profile_data, default_values, cookie_sub)
            checkout_data = get_select_field_values(checkout_data, profile_data, select_fields)

            if check_data(checkout_data, profile_data):
                return checkout_data
        except:
            pass