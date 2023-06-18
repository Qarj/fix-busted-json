# fix-busted-json

Fix broken json using Python.

For Python 3.6+.

This project fixes broken JSON with the following issues:

-   Missing quotes around key names
-   Wrong quotes around key names and strings
    -   Single quotes
    -   Backticks
    -   Escaped double quote
    -   Double escaped double quote
    -   "Smart" i.e. curly quotes
-   Missing commas between key-value pairs and array elements
-   Trailing comma after last key-value pair
-   Concatenation of string fields
-   Replace Python True/False/None with JSON true/false/null

Utility functions are also provided for finding JSON objects in text.

https://github.com/Qarj/fix-busted-json

https://pypi.org/project/fix-busted-json

## Quickstart

```sh
pip install fix-busted-json
```

Make a file called `example_repair_json.py`:

```py
#!/usr/bin/env python3

from fix_busted_json import repair_json

invalid_json = "{ name: 'John' 'age': 30, 'city': 'New' + ' York', }"

fixed_json = repair_json(invalid_json)

print(fixed_json)
```

Note the issues in the invalid JSON:

-   name is unquoted
-   use of single quotes, JSON spec requires double quotes
-   Missing comma
-   Concatenation of string fields - not allowed in JSON
-   Trailing comma

Run it:

```sh
python example_repair_json.py
```

Output:

```json
{ "name": "John", "age": 30, "city": "New York" }
```

## Why

The project was developed originally to find JSON like objects in log files and pretty print them.

More recently this project has been used to find and then fix broken JSON created by large language models such as `gpt-3.5-turbo` and `gpt-4`.

For example a large language model might output a completion like the following:

```txt
Thought: "I need to search for developer jobs in London"
Action: SearchTool
ActionInput: { location: "London", 'title': "developer" }
```

To get back this JSON object with this project is really easy:

```py
#!/usr/bin/env python3

from fix_busted_json import first_json

completion = """Thought: "I need to search for developer jobs in London"
Action: SearchTool
ActionInput: { location: "London", 'title': "developer" }
"""

print(first_json(completion))
```

Output:

```json
{ "location": "London", "title": "developer" }
```

## API

### `repair_json`

```py
#!/usr/bin/env python3

from fix_busted_json import repair_json

invalid_json = "{ name: 'John' }"

fixed_json = repair_json(invalid_json)
```

### log_jsons

Looks for JSON objects in text and logs them, also recursively logging any JSON objects found in the values of the top-level JSON object.

```py
#!/usr/bin/env python3

from fix_busted_json import log_jsons

log_jsons("""some text { key1: true, 'key2': "  { inner: 'value', } " } text { a: 1 } text""")
```

Running it gives output:

```txt
some text
{
  "key1": true,
  "key2": "  { inner: 'value', } "
}

FOUND JSON found in key key2 --->

{
  "inner": "value"
}


 text
{
  "a": 1
}
 text
```

### to_array_of_plain_strings_or_json

Breaks text into an array of plain strings and JSON objects.

```py
#!/usr/bin/env python3

from fix_busted_json import to_array_of_plain_strings_or_json

result = to_array_of_plain_strings_or_json("""some text { key1: true, 'key2': "  { inner: 'value', } " } text { a: 1 } text""")

print(result)
```

Gives output:

```txt
['some text ', '{ "key1": true, "key2": "  { inner: \'value\', } " }', ' text ', '{ "a": 1 }', ' text']
```

### first_json, last_json, largest_json, json_matching

Utility functions for finding JSON objects in text.

```py
#!/usr/bin/env python3
import re
from fix_busted_json import first_json, last_json, largest_json, json_matching

jsons = "text { first: 123 } etc { second_example: 456 } etc { third: 789 } { fourth: 12 }"

print(first_json(jsons))
print(last_json(jsons))
print(largest_json(jsons))
print(json_matching(jsons, re.compile("thi")))
```

Output:

```txt
{ "first": 123 }
{ "fourth": 12 }
{ "second_example": 456 }
{ "third": 789 }
```

## See also

Node version of this project: https://www.npmjs.com/package/log-parsed-json
