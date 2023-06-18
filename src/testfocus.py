import unittest
from index import to_string, to_array_of_plain_strings_or_json, first_json, last_json, largest_json, json_matching
import json
import re

class TestParseJson(unittest.TestCase):

    def assert_is_json(self, json_string):
        try:
            json.loads(json_string)
            return True
        except ValueError:
            return False

    def test_should_cope_with_escaped_double_quotes_used_as_quotes_inside_strings(self):
        input_object = '{\\"@metadata\\":{\\"message\\":\\"{\\\\"url\\\\": \\\\"hey\\\\"}\\"}}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))


if __name__ == '__main__':
    unittest.main()

