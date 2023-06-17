from FixBustedJson import FixBustedJson

some_json = "{ 'name': 'John' 'age': 30, 'city': 'New York' }"

fbj = FixBustedJson(some_json)

# get fixed json string
fixed_string = (fbj.__str__())

