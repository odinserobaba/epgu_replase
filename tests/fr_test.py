import unittest
import uuid
from typing import Tuple, List, Dict, Union
from fr_utils import *

class TestReplaceMatch(unittest.TestCase):
    
    def test_positive_replase_text(self):
        text = '"date": "2024-09-04",'
        pattern = '"date": "([^"]+)",'
        replace_value = "2024-09-06"
        res = replace_match(text, pattern, replace_value)
        self.assertEqual(res, '"date": "2024-09-06",')
        
    def test_positive_replase_uuid(self):
        text = '"id": "5583b1cb-612a-43f1-8011-7f07d1cf3238",'
        pattern = '"id": "([^"]+)"'
        replace_value = str(uuid.uuid4())
        res = replace_match(text, pattern, replace_value)
        self.assertIn(replace_value, res)

class TestParseCommand(unittest.TestCase):

    def test_uuid(self):
        text = '"id": "5583b1cb-612a-43f1-8011-7f07d1cf3238"'
        command_dict: Dict[str, list] = {
            "id": ["uuid4", "any", '"id": "([^"]+)"']
        }
        res = parse_command(command_dict, text)
        self.assertRegex(res, r'"id": "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"')

    def test_replase(self):
        text = '"date": "2024-09-04",'
        command_dict: Dict[str, list] = {
            "date": ["2024-09-06", "replace", '"date": "([^"]+)"']
        }
        res = parse_command(command_dict, text)
        self.assertEqual(res, '"date": "2024-09-06",')