import json
import sys
from FixBustedJson import FixBustedJson

def log(obj):
    if isinstance(obj, (int, float)):
        print(obj)
    elif isinstance(obj, bool):
        print(obj)
    elif isinstance(obj, dict):
        log_pretty(obj)
        print()
    else:
        log_jsons(obj)

def log_jsons(text):
    array = to_array_of_plain_strings_or_json(text)
    for item in array:
        log_pretty(item)
        if is_json(item):
            log_jsons_in_json(item)
    print()

def log_jsons_in_json(item):
    obj = json.loads(item)

    for key in obj:
        if obj[key] and isinstance(obj[key], dict):
            log_jsons_in_json(json.dumps(obj[key]))
        elif can_parse_json(obj[key]):
            print(f"\nFOUND JSON found in key {key} --->")
            log_jsons(obj[key])

def is_json(text):
    try:
        result = json.loads(text)
        if not result:
            return False
        if not isinstance(result, dict):
            return False
        return True
    except Exception:
        return False

def log_pretty(obj):
    try:
        if isinstance(obj, str):
            json_obj = json.loads(obj)
        else:
            json_obj = obj
        print(json.dumps(json_obj, indent=2))
    except Exception:
        print(obj)

def to_string(input):
    parse_json = FixBustedJson(input)
    return str(parse_json)

def to_array_of_plain_strings_or_json(input):
    parse_json = FixBustedJson(input)
    return parse_json.to_array_of_plain_strings_or_json()

def can_parse_json(input):
    parse_json = FixBustedJson(input)
    try:
        str(parse_json)
        return True
    except Exception:
        return False

def first_json(input):
    parse_json = FixBustedJson(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    for item in result:
        if can_parse_json(item):
            return item
    return ""

def last_json(input):
    parse_json = FixBustedJson(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    for i in range(len(result) - 1, -1, -1):
        if can_parse_json(result[i]):
            return result[i]
    return ""

def largest_json(input):
    parse_json = FixBustedJson(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    largest = ""
    for item in result:
        if can_parse_json(item) and len(item) > len(largest):
            largest = item
    return largest

def json_matching(input, regex):
    parse_json = FixBustedJson(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    for item in result:
        if can_parse_json(item) and regex.search(item):
            return item
    return ""
