#!/usr/bin/env python3
import re
from fix_busted_json import first_json, last_json, largest_json, json_matching

jsons = "text { first: 123 } etc { second_example: 456 } etc { third: 789 } { fourth: 12 }"

print(first_json(jsons))
print(last_json(jsons))
print(largest_json(jsons))
print(json_matching(jsons, re.compile("thi")))
