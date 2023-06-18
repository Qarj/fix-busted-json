#!/usr/bin/env python3

from fix_busted_json import repair_json

invalid_json = "{ name: 'John' 'age': 30, 'city': 'New' + ' York', }"

fixed_json = repair_json(invalid_json)

print(fixed_json)