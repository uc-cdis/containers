import unittest

from utils import captured_output

from vlmd_submission_tools.common import mapping_utils

class TestMappingUtils(unittest.TestCase):


    def test_split_str_array(self):
        string="foo|bar"
        expected=["foo", "bar"]
        self.assertEqual(mapping_utils.split_str_array(string), expected)
        sep="#"
        string="foo#bar"
        expected=["foo", "bar"]
        self.assertEqual(mapping_utils.split_str_array(string,sep), expected)


    def test_map_keys_vals(self):
        keys=['key1', 'key2', 'key3']
        vals=['val1', 'val2', 'val3']
        expected={'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
        self.assertEqual(mapping_utils.map_keys_vals(keys,vals), expected)


    def test_split_and_map(self):
        string="1=foo|2=bar|3=flim"
        prop = {
            'items': {
                'properties': {
                    'key1': 'val1',
                    'key2': 'val2',
                    'key3': 'val3'
                }
            }
        }
        expected=[
            {'key1': '1', 'key2': 'foo'},
            {'key1': '2', 'key2': 'bar'},
            {'key1': '3', 'key2': 'flim'}
        ]
        self.assertEqual(mapping_utils.split_and_map(string,prop), expected)


    def test_loads_dict(self):
        string="1=foo|2=bar|3=flim"
        expected={'1': 'foo', '2': 'bar', '3': 'flim'}
        self.assertEqual(mapping_utils.loads_dict(string), expected)
        string2="1_foo#2_bar#3_flim"
        result = mapping_utils.loads_dict(string2,item_sep='#',key_val_sep='_')
        self.assertEqual(result, expected)


    def test_to_bool(self):
        test_vals=['True', 'true', '1', 'Yes', 'Y', 'Required']
        for val in test_vals:
            self.assertTrue(mapping_utils.to_bool(val))
        test_vals=['False', 'false', '0', 'No', 'N', 'Not Required']
        for val in test_vals:
            self.assertFalse(mapping_utils.to_bool(val))
        test_vals=['Foo', 'Bar']
        for val in test_vals:
            self.assertEqual(mapping_utils.to_bool(val), "")


    def test_join_dict_vals(self):
        sep="|"
        dict={'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
        expected="val1|val2|val3"
        self.assertEqual(mapping_utils.join_dictvals(dict,sep), expected)
