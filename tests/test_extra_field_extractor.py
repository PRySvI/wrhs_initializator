import unittest

from extra_field_extractor import get_all_extra_fields_inserts_request


class Testing(unittest.TestCase):
    def test_string(self):
        print(get_all_extra_fields_inserts_request())
