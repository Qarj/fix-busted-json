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

    def test_to_string_function_exists(self):
        self.assertIsNotNone(to_string)

    def test_should_return_valid_json_string_from_inspected_output(self):
        input = "{ test: 'test', array: ['test', { test: 'test' }] }"
        result = to_string(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_array_of_strings_and_json_strings(self):
        input = "text before { test: 'test', array: ['test', { test: 'test' }] } text after"
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'text before ')
        self.assertEqual(result[1], '{ "test": "test", "array": ["test", { "test": "test" }] }')
        self.assertEqual(result[2], ' text after')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_return_first_valid_json_object(self):
        input = "text before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        result = first_json(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_last_valid_json_object(self):
        input = "text before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        result = last_json(input)
        expected = '{ "hey": 1 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_largest_valid_json_object(self):
        input = "text { gday: 'hi' } before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        result = largest_json(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_json_object_matching_regular_expression(self):
        input = "text { gday: 'hi' } before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        pattern = re.compile("hey")
        result = json_matching(input, pattern)
        expected = '{ "hey": 1 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_brace_in_string(self):
        input = 'real json {"value":["closing brace }"]}'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'real json ')
        self.assertEqual(result[1], '{ "value": ["closing brace }"] }')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_cope_with_double_quote_in_string(self):
        input = 'real json {"value":["double quote \\"test"]}'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'real json ')
        self.assertEqual(result[1], '{ "value": ["double quote \\"test"] }')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_parse_an_array_of_numbers(self):
        input = 'real json { "test": [ 1, 2, 3] }'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'real json ')
        self.assertEqual(result[1], '{ "test": [1, 2, 3] }')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_cope_with_empty_object(self):
        input = 'is json {} abc'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'is json ')
        self.assertEqual(result[1], '{  }')
        self.assertEqual(result[2], ' abc')

    def test_should_throw_on_unexpected_end_of_quoted_key_or_string(self):
        with self.assertRaises(IndexError):
            to_string('{"}')

    def test_should_cope_with_all_kinds_of_whitespace(self):
        input = ' {  \t "test"\t: \t 123 \r \n }'
        result = to_string(input)
        expected = '{ "test": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_single_quoted_string_to_double_quotes_needs_to_quote_double_quotes(self):
        input = """{ 'abc "': 'test' }"""
        result = to_string(input)
        expected = '{ "abc \\"": "test" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_single_quoted_string_to_double_quotes_needs_to_unquote_single_quotes(self):
        with open('./singlequoted.txt', 'r') as file:
            input = file.read()
        result = to_string(input)
        expected = """{ "abc '": "test'", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_backtick_quoted_string_to_double_quotes_needs_to_fix_quotes(self):
        input = "{ `abc \'\"`: `test\'\"`, 'key': 123}"
        result = to_string(input)
        expected = """{ "abc '\\"": "test'\\"", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_backticked_quoted_string_to_double_quotes_needs_to_unquote_single_quotes_but_not_double(self):
        with open('./backticked.txt', 'r') as file:
            input = file.read()
        result = to_string(input)
        expected = """{ "abc '\\"`": "test`'\\"", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_cope_with_trailing_comma_in_key_value_pairs_for_object(self):
        input = '{ "abc": 123, }'
        result = to_string(input)
        expected = '{ "abc": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

if __name__ == '__main__':
    unittest.main()

