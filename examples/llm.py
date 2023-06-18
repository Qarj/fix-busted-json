#!/usr/bin/env python3

from fix_busted_json import first_json

completion = """Thought: "I need to search for developer jobs in London"
Action: SearchTool
ActionInput: { location: "London", 'title': "developer" }
"""

json_object = first_json(completion)
print(json_object)