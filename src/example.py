from index import to_string

some_json = "{ 'name': 'John' 'age': 30, 'city': 'New York' }"

fixed_string = to_string(some_json)

print(fixed_string)