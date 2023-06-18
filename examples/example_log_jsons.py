#!/usr/bin/env python3

from fix_busted_json import log_jsons

log_jsons("""some text { key1: true, 'key2': "  { inner: 'value', } " } text { a: 1 } text""")
