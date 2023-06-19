#!/usr/bin/env python3

import unittest
from fix_busted_json import repair_json, to_array_of_plain_strings_or_json, first_json, last_json, largest_json, json_matching
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
        self.assertIsNotNone(repair_json)

    def test_should_return_valid_json_string_from_inspected_output(self):
        input = "{ test: 'test', array: ['test', { test: 'test' }] }"
        result = repair_json(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_parse_a_number(self):
        result = repair_json('{ "number": 123 }')
        self.assertEqual(result, '{ "number": 123 }')

    def test_should_throw_error_when_given_an_unquoted_string_value(self):
        result = "{ test: postgres }"
        with self.assertRaises(ValueError, msg="Primitive not recognized, must start with f, t, n, or be numeric"):
            repair_json(result)

    def test_should_throw_with_unquoted_string_value_in_array(self):
        result = "{ test: [1, 2, postgres] }"
        with self.assertRaises(ValueError, msg="Primitive not recognized, must start with f, t, n, or be numeric"):
            repair_json(result)

    def test_should_throw_error_when_a_number_starts_with_zero(self):
        result = "{ test: 0123 }"
        with self.assertRaises(ValueError, msg="Number cannot have redundant leading 0"):
            repair_json(result)

    def test_should_cope_with_negative_numbers(self):
        result = "{ test: -123 }"
        result = repair_json(result)
        self.assertEqual(result, '{ "test": -123 }')

    def test_should_cope_with_a_negative_decimal(self):
        result = "{ test: -0.123 }"
        result = repair_json(result)
        self.assertEqual(result, '{ "test": -0.123 }')

    def test_should_cope_with_a_decimal_starting_with_zero(self):
        result = "{ test: 0.123 }"
        result = repair_json(result)
        self.assertEqual(result, '{ "test": 0.123 }')

    def test_should_throw_error_with_a_fake_primitive_starting_with_f(self):
        result = "{ test: fake }"
        with self.assertRaises(ValueError, msg="Keyword not recognized, must be true, false, null or none"):
            repair_json(result)

    def test_should_throw_correct_error_with_incorrect_primitive_f(self):
        result = "{test:f}"
        with self.assertRaises(ValueError, msg="Keyword not recognized, must be true, false, null or none"):
            repair_json(result)

    def test_should_throw_correct_error_when_a_number_contains_a_letter(self):
        result = "{ test: 123a }"
        with self.assertRaises(Exception, msg="Expected colon"):
            repair_json(result)

    def test_should_parse_a_decimal(self):
        result = repair_json('{ "decimal": 123.456 }')
        self.assertEqual(result, '{ "decimal": 123.456 }')

    def test_should_parse_true(self):
        result = repair_json('{ "boolean": true }')
        self.assertEqual(result, '{ "boolean": true }')

    def test_should_parse_false(self):
        result = repair_json('{ "boolean": false }')
        self.assertEqual(result, '{ "boolean": false }')

    def test_should_parse_null(self):
        result = repair_json('{ "null": null }')
        self.assertEqual(result, '{ "null": null }')


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
            repair_json('{"}')

    def test_should_cope_with_all_kinds_of_whitespace(self):
        input = ' {  \t "test"\t: \t 123 \r \n }'
        result = repair_json(input)
        expected = '{ "test": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_single_quoted_string_to_double_quotes_needs_to_quote_double_quotes(self):
        input = """{ 'abc "': 'test' }"""
        result = repair_json(input)
        expected = '{ "abc \\"": "test" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_single_quoted_string_to_double_quotes_needs_to_unquote_single_quotes(self):
        with open('tests/singlequoted.txt', 'r') as file:
            input = file.read()
        result = repair_json(input)
        expected = """{ "abc '": "test'", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_backtick_quoted_string_to_double_quotes_needs_to_fix_quotes(self):
        input = "{ `abc \'\"`: `test\'\"`, 'key': 123}"
        result = repair_json(input)
        expected = """{ "abc '\\"": "test'\\"", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_backticked_quoted_string_to_double_quotes_needs_to_unquote_single_quotes_but_not_double(self):
        with open('tests/backticked.txt', 'r') as file:
            input = file.read()
        result = repair_json(input)
        expected = """{ "abc '\\"`": "test`'\\"", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_cope_with_trailing_comma_in_key_value_pairs_for_object(self):
        input = '{ "abc": 123, }'
        result = repair_json(input)
        expected = '{ "abc": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_cope_with_circular_references(self):
        scenario = """{
    abc: <ref *1> {
        abc: 123,
        def: 'test',
        ghi: { jkl: 'test' },
        xyz: { zzz: 123, jj: 'test', abc: [Circular *1] }
    },
    def: <ref *2> {
        zzz: 123,
        jj: 'test',
        abc: <ref *1> {
        abc: 123,
        def: 'test',
        ghi: { jkl: 'test' },
        xyz: [Circular *2]
        }
    }
    }"""
        result = repair_json(scenario)
        self.assertIn('"Circular"', result)
        self.assertTrue(self.assert_is_json(result))

    def test_can_cope_with_stringified_strings(self):
        scenario = '{\n  \"abc\": 123\n  }\n}'
        result = repair_json(scenario)
        expected = '{ "abc": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_empty_object_is_valid_json(self):
        scenario = '{}'
        result = repair_json(scenario)
        self.assertTrue(self.assert_is_json(result))

    def test_should_play_nice_with_empty_objects(self):
        scenario = '{ "t": [], "a": {} }'
        result = repair_json(scenario)
        expected = '{ "t": [], "a": {  } }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_overly_stringified_objects(self):
        object = {
            'arr"ay': [
                1,
                {
                    'obj"ec\'}t': { "\n\nk\"\'ey": "\"\"''',value" },
                },
                [],
                {},
                True,
                None,
            ],
        }
        scenario = json.dumps(json.dumps(json.dumps(json.dumps(object))))
        result = repair_json(scenario)
        self.assertTrue(self.assert_is_json(result))

    def test_should_concatenate_strings_with_plus(self):
        obj = '{ "abc": "test" + "test2" }'
        result = repair_json(obj)
        expected = '{ "abc": "testtest2" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_concatenate_strings_with_plus_and_preserve_whitespace(self):
        obj = '{ "abc": "test" + "test2" + "test3" }'
        result = repair_json(obj)
        expected = '{ "abc": "testtest2test3" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_concatenate_strings_with_different_quotes(self):
        obj = '{ "abc": \'test\' + `test2` + "test3" + \\"test4\\" }'
        result = repair_json(obj)
        expected = '{ "abc": "testtest2test3test4" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_python_true(self):
        obj = '{ "abc": True }'
        result = repair_json(obj)
        expected = '{ "abc": true }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_python_false(self):
        input_object = '{ "abc": False }'
        result = repair_json(input_object)
        expected = '{ "abc": false }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_change_none_primitive_to_null(self):
        input_object = '{ "abc": None }'
        result = repair_json(input_object)
        expected = '{ "abc": null }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_change_noNe_primitive_to_null(self):
        input_object = "{'intent': {'slots': {'location': noNe}, 'confirmationState': 'None', 'name': 'JobSearch', 'state': 'InProgress'}, 'nluConfidence': 0.8}"
        result = repair_json(input_object)
        expected = '{ "intent": { "slots": { "location": null }, "confirmationState": "None", "name": "JobSearch", "state": "InProgress" }, "nluConfidence": 0.8 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_treat_space_in_key_name_as_terminator_if_no_in_quotes(self):
        input_object = " { toString } "
        with self.assertRaises(Exception, msg="Expected colon"):
            repair_json(input_object)

    def test_should_support_null_key_name(self):
        input_object = " { [null]: 'test' } "
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_bug_should_support_newline_after_object_before_array_end(self):
        input_object = """{
        savedJobs: [
            {
                external: false
            }
        ]
    }"""
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_support_trailing_comma_in_array_1(self):
        input_object = """{
        savedJobs: [
            {
                external: false
            },
        ]
    }"""
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_support_trailing_comma_in_array_2(self):
        input_object = "{ arr: [1,2,3,]}"
        result = repair_json(input_object)
        expected = '{ "arr": [1, 2, 3] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_escaped_double_quotes_used_as_quotes_aka_kibana(self):
        input_object = '{\\"@metadata\\":{\\"beat\\":\\"filebeat\\"}}'
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_escaped_double_quotes_used_as_quotes_inside_strings(self):
        input_object = '{\\"@metadata\\":{\\"message\\":\\"{\\\\"url\\\\": \\\\"hey\\\\"}\\"}}'
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_double_escaped_double_quotes_used_as_quotes_case_1(self):
        input_object = '{ \\\\"test\\\\": \\\\"test1\\\\" }'
        result = repair_json(input_object)
        expected = '{ "test": "test1" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_double_escaped_double_quotes_used_as_quotes_case_2(self):
        input_object = '{\\"@metadata\\":{\\"message\\":\\"{\\\\"url\\\\": \\\\"hey\\\\"}\\"}}'
        result = repair_json(input_object)
        expected = '{ "@metadata": { "message": "{\\"url\\": \\"hey\\"}" } }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_pretty_formatted_sloping_double_quotes_as_output_by_word(self):
        input_object = '{\n"abc": “test”\n}'
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_pretty_formatted_sloping_double_quotes_as_output_by_word_case_2(self):
        input_object = '{“abc”: “def”}'
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_stack_overflow_json(self):
        input_object = '{\nstaus: "Success",\nid: 1,\ndata: [{\'Movie\':\'kung fu panda\',\'% viewed\': 50.5},{\'Movie\':\'kung fu panda 2\',\'% viewed\':1.5}],\nmetadata: {\'filters\':[\'Movie\', \'Percentage Viewed\' ] , \'params\':{\'content\':\'Comedy\', \'type\': \'Movie\'}}\n}'
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_insert_missing_commas_between_key_value_pairs(self):
        input_object = '{\n"abc": "def"\n"ghi": "jkl"\n}'
        result = repair_json(input_object)
        expected = '{ "abc": "def", "ghi": "jkl" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_insert_missing_commas_between_key_value_pairs_case_2(self):
        input_object = '{\n"abc": "def"\n"ghi": "jkl"\n"mno": "pqr"\n}'
        result = repair_json(input_object)
        expected = '{ "abc": "def", "ghi": "jkl", "mno": "pqr" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_insert_missing_commas_between_array_elements(self):
        input_object = '{\n"abc": [\n"def"\n"ghi" 3 true null\n]\n}'
        result = repair_json(input_object)
        expected = '{ "abc": ["def", "ghi", 3, true, null] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_error_the_right_way_given_broken_json(self):
        input_object = '{ "test": "bad  { "test": "good" }'
        with self.assertRaises(Exception, msg="Expected colon"):
            repair_json(input_object)

    def test_should_cope_with_a_difficult_scenario(self):
        input_object = '{ \nvalue: true peter: \'fun\' number: 3 somekey: "a string"\narray: [ 2 9234 98234 9 9213840  98213409 98234]\n}'
        result = repair_json(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_unquoted_single_quote_inside_single_quoted_string_if_an_s_follows(self):
        input_object = "{ 'test': 'test's' }"
        result = repair_json(input_object)
        expected = '{ "test": "test\'s" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))


if __name__ == '__main__':
    unittest.main()

