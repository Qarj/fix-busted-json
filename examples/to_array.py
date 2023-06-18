#!/usr/bin/env python3

from fix_busted_json import to_array_of_plain_strings_or_json

result = to_array_of_plain_strings_or_json("""some text { key1: true, 'key2': "  { inner: 'value', } " } text { a: 1 } text""")

print(result)