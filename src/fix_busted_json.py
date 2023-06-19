#!/usr/bin/env python3

import json
import re

def log(obj):
    if isinstance(obj, (int, float)):
        print(obj)
    elif isinstance(obj, bool):
        print(obj)
    elif isinstance(obj, dict):
        log_pretty(obj)
        print()
    else:
        log_jsons(obj)

def log_jsons(text):
    array = to_array_of_plain_strings_or_json(text)
    for item in array:
        log_pretty(item)
        if is_json(item):
            log_jsons_in_json(item)
    print()

def log_jsons_in_json(item):
    obj = json.loads(item)

    for key in obj:
        if obj[key] and isinstance(obj[key], dict):
            log_jsons_in_json(json.dumps(obj[key]))
        elif can_parse_json(obj[key]):
            print(f"\nFOUND JSON found in key {key} --->")
            log_jsons(obj[key])

def is_json(text):
    try:
        result = json.loads(text)
        if not result:
            return False
        if not isinstance(result, dict):
            return False
        return True
    except Exception:
        return False

def log_pretty(obj):
    try:
        if isinstance(obj, str):
            json_obj = json.loads(obj)
        else:
            json_obj = obj
        print(json.dumps(json_obj, indent=2))
    except Exception:
        print(obj)

def repair_json(input):
    parse_json = JsonParser(input)
    return parse_json.repair_json()

def to_array_of_plain_strings_or_json(input):
    parse_json = JsonParser(input)
    return parse_json.to_array_of_plain_strings_or_json()

def can_parse_json(input):
    parse_json = JsonParser(input)
    try:
        parse_json.repair_json()
        return True
    except Exception:
        return False

def first_json(input):
    parse_json = JsonParser(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    for item in result:
        if can_parse_json(item):
            return item
    return ""

def last_json(input):
    parse_json = JsonParser(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    for i in range(len(result) - 1, -1, -1):
        if can_parse_json(result[i]):
            return result[i]
    return ""

def largest_json(input):
    parse_json = JsonParser(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    largest = ""
    for item in result:
        if can_parse_json(item) and len(item) > len(largest):
            largest = item
    return largest

def json_matching(input, regex):
    parse_json = JsonParser(input)
    result = parse_json.to_array_of_plain_strings_or_json()
    for item in result:
        if can_parse_json(item) and regex.search(item):
            return item
    return ""

class JsonParser:
    def __init__(self, input):
        self.inspected = self.de_stringify(input)
        self.reset_pointer()
        self.debug = False

    def reset_pointer(self):
        self.position = 0
        self.quoted = ''
        self.checkpoint = 0
        self.checkpoint_quoted = ''
        self.quoted_last_comma_position = None

    def set_checkpoint(self):
        if self.debug:
            print('setCheckpoint', self.position, self.inspected[self.position])
        self.checkpoint = self.position
        self.checkpoint_quoted = self.quoted

    def repair_json(self):
        self.reset_pointer()
        self.eat_object()
        return self.quoted

    def de_stringify(self, string):
        try:
            result = json.loads(string)
            if isinstance(result, str):
                return self.de_stringify(result)
            return string
        except Exception as e:
            return string

    def to_array_of_plain_strings_or_json(self):
        result = []
        self.reset_pointer()
        recovery_position = 0
        while self.position < len(self.inspected):
            self.quoted = ''
            self.eat_plain_text()
            result.append(self.quoted)
            self.quoted = ''
            if self.position >= len(self.inspected):
                break
            if self.inspected[self.position] == '{':
                recovery_position = self.position + 1

                try:
                    self.eat_object()
                except Exception as e:
                    self.quoted += '{'
                    self.position = recovery_position

            result.append(self.quoted)

        return result

    def eat_plain_text(self):
        while self.position < len(self.inspected) and self.inspected[self.position] != '{':
            if self.debug:
                print('eat_plain_text', self.position, self.inspected[self.position])
            self.quoted += self.inspected[self.position]
            self.position += 1

    def eat_object(self):
        if self.debug:
            print('eat_object', self.position, self.inspected[self.position])
        self.eat_whitespace()
        self.eat_open_brace()
        self.eat_key_value_pairs()
        self.eat_whitespace()
        self.eat_close_brace()

    def eat_key_value_pairs(self):
        if self.debug:
            print('eat_key_value_pairs', self.position, self.inspected[self.position])
        while True:
            self.eat_whitespace()
            if self.inspected[self.position] == '}':
                self.remove_trailing_comma_if_present()
                break
            self.quoted_last_comma_position = None
            self.eat_key()
            self.eat_whitespace()
            self.eat_colon()
            self.eat_whitespace()
            self.eat_reference_optional()
            self.eat_whitespace()
            self.eat_value()
            self.quoted_last_comma_position = None
            self.eat_whitespace()

            if self.inspected[self.position] == ',':
                self.eat_comma()
            elif self.inspected[self.position] != '}':
                self.quoted += ', '

    def eat_reference_optional(self):
        if self.inspected[self.position] == '<':
            self.eat_reference()

    def eat_reference(self):
        self.set_checkpoint()
        self.eat_open_angle_bracket()
        self.eat_whitespace()
        self.eat_ref()
        self.eat_whitespace()
        self.eat_asterisk()
        self.eat_whitespace()
        self.eat_reference_number()
        self.eat_whitespace()
        self.eat_close_angle_bracket()

    def eat_open_angle_bracket(self):
        if self.inspected[self.position] != '<':
            raise Exception('Expected open angle bracket')
        self.position += 1

    def eat_ref(self):
        if self.inspected[self.position] != 'r':
            raise Exception('Expected r')
        self.position += 1
        if self.inspected[self.position] != 'e':
            raise Exception('Expected e')
        self.position += 1
        if self.inspected[self.position] != 'f':
            raise Exception('Expected f')
        self.position += 1

    def eat_asterisk(self):
        if self.inspected[self.position] != '*':
            raise Exception('Expected asterisk')
        self.position += 1

    def eat_reference_number(self):
        number_regex = re.compile(r'[0-9]')
        while number_regex.match(self.inspected[self.position]):
            self.position += 1

    def eat_close_angle_bracket(self):
        if self.inspected[self.position] != '>':
            raise Exception('Expected close angle bracket')
        self.position += 1

    def eat_comma_post_value_optional(self):
        if self.inspected[self.position] == ',':
            self.eat_comma()
            return True
        return False

    def eat_whitespace(self):
        whitespace_regex = re.compile(r'\s')
        while whitespace_regex.match(self.inspected[self.position]):
            self.position += 1

    def eat_open_brace(self):
        if self.debug:
            print('eat_open_brace', self.position, self.inspected[self.position])
        if self.inspected[self.position] != '{':
            raise Exception('Expected open brace')
        self.quoted += self.inspected[self.position] + ' '
        self.position += 1

    def eat_close_brace(self):
        if self.debug:
            print('eat_close_brace', self.position, self.inspected[self.position])
        if self.inspected[self.position] != '}':
            raise Exception('Expected close brace')
        self.quoted += ' ' + self.inspected[self.position]
        self.position += 1

    def eat_key(self):
        if self.debug:
            print('eat_key', self.position, self.inspected[self.position])
        if self.get_quote():
            self.eat_quoted_key()
        else:
            self.eat_unquoted_key()

    def get_quote(self):
        if self.inspected[self.position] == "'":
            return "'"
        if self.inspected[self.position] == '"':
            return '"'
        if self.inspected[self.position] == '`':
            return '`'
        if self.inspected[self.position] == '“':
            return '”'
        if self.inspected[self.position] == '\\' and self.inspected[self.position + 1] == '"':
            return '\\"'
        if (
            self.inspected[self.position] == '\\' and
            self.inspected[self.position + 1] == '\\' and
            self.inspected[self.position + 2] == '"'
        ):
            return '\\\\"'
        return False

    def check_quote(self, quote):
        if len(quote) == 1:
            return self.inspected[self.position] == quote
        if len(quote) == 2:
            return (
                self.inspected[self.position] == quote[0] and
                self.inspected[self.position + 1] == quote[1]
            )
        if len(quote) == 3:
            return (
                self.inspected[self.position] == quote[0] and
                self.inspected[self.position + 1] == quote[1] and
                self.inspected[self.position + 2] == quote[2]
            )
        return False

    def eat_quote_additional(self, quote):
        eat_extra = len(quote) - 1
        for _ in range(eat_extra):
            self.position += 1

    def eat_quoted_key(self):
        if self.debug:
            print('eat_quoted_key', self.position, self.inspected[self.position])
        self.set_checkpoint()
        self.throw_if_json_special_character(self.inspected[self.position])
        quote = self.get_quote()
        self.quoted += '"'
        self.position += 1
        self.eat_quote_additional(quote)
        while not self.check_quote(quote):
            self.eat_char_or_escaped_char(quote)
        self.quoted += '"'
        self.position += 1
        self.eat_quote_additional(quote)

    def eat_unquoted_key(self):
        if self.debug:
            print('eat_unquoted_key', self.position, self.inspected[self.position])
        self.set_checkpoint()
        if self.inspected[self.position] == '[':
            return self.eat_null_key()
        self.throw_if_json_special_character(self.inspected[self.position])
        self.quoted += '"'
        while self.inspected[self.position] != ':' and self.inspected[self.position] != ' ':
            if self.get_quote():
                raise Exception('Unexpected quote in unquoted key')
            self.quoted += self.inspected[self.position]
            self.position += 1
        self.quoted += '"'

    def eat_null_key(self):
        if self.debug:
            print('eat_null_key', self.position, self.inspected[self.position])
        if self.inspected[self.position] != '[':
            raise Exception('Expected open bracket')
        self.position += 1
        if self.inspected[self.position].lower() != 'n':
            raise Exception('Expected n')
        self.position += 1
        if self.inspected[self.position].lower() != 'u':
            raise Exception('Expected u')
        self.position += 1
        if self.inspected[self.position].lower() != 'l':
            raise Exception('Expected l')
        self.position += 1
        if self.inspected[self.position].lower() != 'l':
            raise Exception('Expected l')
        self.position += 1
        if self.inspected[self.position] != ']':
            raise Exception('Expected close bracket')
        self.position += 1
        self.quoted += '"null"'

    def throw_if_json_special_character(self, char):
        if char in ['{', '}', '[', ']', ':', ',']:
            raise Exception(f'Unexpected character {char} at position {self.position}')

    def eat_colon(self):
        if self.debug:
            print('eat_colon', self.position, self.inspected[self.position])
        if self.inspected[self.position] != ':':
            raise Exception('Expected colon')
        self.quoted += self.inspected[self.position] + ' '
        self.position += 1

    def eat_value(self):
        if self.debug:
            print('eat_value', self.position, self.inspected[self.position])
        if self.inspected[self.position] == '{':
            self.eat_object()
        elif self.get_quote():
            self.eat_string()
            self.eat_concatenated_strings()
        elif self.inspected[self.position] == '[':
            self.eat_array()
        else:
            self.eat_primitive()

    def eat_string(self):
        if self.debug:
            print('eat_string', self.position, self.inspected[self.position])
        self.set_checkpoint()
        quote = self.get_quote()
        self.quoted += '"'
        self.position += 1
        self.eat_quote_additional(quote)
        while not self.is_end_quote_making_allowance_for_unescaped_single_quote(quote):
            self.eat_char_or_escaped_char(quote)
        self.quoted += '"'
        self.position += 1
        self.eat_quote_additional(quote)

    def eat_concatenated_strings(self):
        if self.debug:
            print('eat_concatenated_strings', self.position, self.inspected[self.position])
        virtual_position = self.eat_virtual_whitespace(self.position + 1)
        if self.inspected[virtual_position] != '+':
            return

        self.position = virtual_position + 1
        self.eat_whitespace()
        self.quoted = self.quoted[:-1]

        quote = self.get_quote()
        self.position += 1
        self.eat_quote_additional(quote)
        while not self.is_end_quote_making_allowance_for_unescaped_single_quote(quote):
            self.eat_char_or_escaped_char(quote)
        self.quoted += '"'
        self.position += 1
        self.eat_quote_additional(quote)

        self.eat_concatenated_strings()

    def is_end_quote_making_allowance_for_unescaped_single_quote(self, quote):
        if quote != "'":
            return self.check_quote(quote)
        try:
            if self.check_quote(quote) and self.inspected[self.position + 1] == 's':
                return False
        except IndexError:
            pass
        return self.check_quote(quote)

    def eat_virtual_whitespace(self, virtual_position):
        if virtual_position >= len(self.inspected):
            return virtual_position - 1
        whitespace_regex = re.compile(r'\s')
        while virtual_position < len(self.inspected) and whitespace_regex.match(self.inspected[virtual_position]):
            virtual_position += 1
        return virtual_position

    def is_double_escaped_double_quote(self):
        if self.position + 2 >= len(self.inspected):
            return False
        return (
            self.inspected[self.position] == '\\' and
            self.inspected[self.position + 1] == '\\' and
            self.inspected[self.position + 2] == '"'
        )

    def eat_char_or_escaped_char(self, quote):
        if self.debug:
            print('eat_char_or_escaped_char', self.position, self.inspected[self.position])
        if self.position >= len(self.inspected):
            raise Exception('Unexpected end of quoted key or string')
        if self.debug:
            print(
                'eatCharOrEscapedChar',
                self.position,
                self.inspected[self.position],
                ' ' + str(ord(self.inspected[self.position])),
            )
        if not self.check_quote(quote) and self.inspected[self.position] == '\\':
            if self.is_double_escaped_double_quote():
                self.position += 1
            if (quote == "'" or quote == '`') and self.inspected[self.position + 1] == quote:
                pass
            else:
                self.quoted += self.inspected[self.position]
            self.position += 1
        if (quote == "'" or quote == '`') and self.inspected[self.position] == '"':
            self.quoted += '\\'
        self.quoted += self.inspected[self.position]
        self.position += 1

    def eat_array(self):
        if self.debug:
            print('eat_array', self.position, self.inspected[self.position])
        if self.inspected[self.position] != '[':
            raise Exception('Expected array')
        self.quoted += self.inspected[self.position]
        self.position += 1

        while True:
            self.eat_whitespace()
            self.eat_circular_optional()
            if self.inspected[self.position] == ']':
                self.remove_trailing_comma_if_present()
                break
            self.quoted_last_comma_position = None
            self.eat_value()
            self.eat_whitespace()

            if self.inspected[self.position] == ',':
                self.eat_comma()
            elif self.inspected[self.position] != ']':
                self.quoted += ', '

        self.eat_close_bracket()

    def remove_trailing_comma_if_present(self):
        if self.quoted_last_comma_position:
            self.quoted = (
                self.quoted[:self.quoted_last_comma_position] +
                self.quoted[self.quoted_last_comma_position + 2:]
            )
        self.quoted_last_comma_position = None

    def eat_circular_optional(self):
        if (
            self.inspected[self.position] == 'C' and
            self.inspected[self.position + 1] == 'i' and
            self.inspected[self.position + 2] == 'r' and
            self.inspected[self.position + 3] == 'c' and
            self.inspected[self.position + 4] == 'u' and
            self.inspected[self.position + 5] == 'l' and
            self.inspected[self.position + 6] == 'a' and
            self.inspected[self.position + 7] == 'r'
        ):
            self.eat_circular()

    def eat_circular(self):
        test_regex = re.compile(r'[Circular *\d]')
        while test_regex.match(self.inspected[self.position]):
            self.position += 1
        self.quoted += '"Circular"'

    def eat_comma(self):
        if self.debug:
            print('eat_comma', self.position, self.inspected[self.position])
        if self.inspected[self.position] != ',':
            raise Exception('Expected comma')
        self.quoted += self.inspected[self.position] + ' '
        self.quoted_last_comma_position = len(self.quoted) - 2
        self.position += 1
        return True

    def eat_close_bracket(self):
        if self.inspected[self.position] != ']':
            raise Exception('Expected close bracket')
        self.quoted += self.inspected[self.position]
        self.position += 1
        return False

    # def eat_primitive(self):
    #     self.set_checkpoint()

    #     if (
    #         self.inspected[self.position].lower() == 'f' and
    #         self.inspected[self.position + 1].lower() == 'a' and
    #         self.inspected[self.position + 2].lower() == 'l' and
    #         self.inspected[self.position + 3].lower() == 's' and
    #         self.inspected[self.position + 4].lower() == 'e'
    #     ):
    #         return self.eat_false()

    #     if (
    #         self.inspected[self.position].lower() == 'n' and
    #         self.inspected[self.position + 1].lower() == 'o' and
    #         self.inspected[self.position + 2].lower() == 'n' and
    #         self.inspected[self.position + 3].lower() == 'e'
    #     ):
    #         return self.eat_none()

    #     if (
    #         self.inspected[self.position].lower() == 't' and
    #         self.inspected[self.position + 1].lower() == 'r' and
    #         self.inspected[self.position + 2].lower() == 'u' and
    #         self.inspected[self.position + 3].lower() == 'e'
    #     ):
    #         return self.eat_true()

    #     primitive_regex = re.compile(r'([0-9a-zA-Z-.])')
    #     while primitive_regex.match(self.inspected[self.position]):
    #         self.quoted += self.inspected[self.position]
    #         self.position += 1

    # def eat_false(self):
    #     self.quoted += 'false'
    #     self.position += 5

    # def eat_none(self):
    #     self.quoted += 'null'
    #     self.position += 4

    # def eat_true(self):
    #     self.quoted += 'true'
    #     self.position += 4

    def eat_primitive(self):
        self.set_checkpoint()
        if self.debug:
            print('eatPrimitive', self.position, self.inspected[self.position])

        lower_char = self.inspected[self.position].lower()
        if lower_char == 'f' or lower_char == 't' or lower_char == 'n':
            self.eat_keyword()
        elif self.is_number_start_char(lower_char):
            self.eat_number()
        else:
            raise ValueError('Primitive not recognized, must start with f, t, n, or be numeric')

    def is_number_start_char(self, char):
        return char and re.match(r'[\-0-9]', char)

    def eat_keyword(self):
        lower_substring = self.inspected[self.position:self.position + 5].lower()

        if lower_substring.startswith('false'):
            self.log('eatFalse')
            self.quoted += 'false'
            self.position += 5
        elif lower_substring.startswith('true'):
            self.log('eatTrue')
            self.quoted += 'true'
            self.position += 4
        elif lower_substring.startswith('none') or lower_substring.startswith('null'):
            self.log('eatNull')
            self.quoted += 'null'
            self.position += 4
        else:
            raise ValueError('Keyword not recognized, must be true, false, null or none')

    def eat_number(self):
        number_str = ''

        self.log('eatNumber')

        while self.is_number_char(self.inspected[self.position]):
            number_str += self.inspected[self.position]
            self.position += 1

        check_str = number_str
        if check_str.startswith('-'):
            check_str = check_str[1:]

        if len(check_str) > 1 and check_str.startswith('0') and not check_str.startswith('0.'):
            raise ValueError('Number cannot have redundant leading 0')

        self.quoted += number_str

    def is_number_char(self, char):
        return char and re.match(r'[\-0-9.]', char)
    
    def log(self, message):
        if self.debug:
            print(message, self.position, self.inspected[self.position])

