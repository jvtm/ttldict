"""
Unit tests for TTLDict
"""

from unittest import TestCase
from ttldict import TTLDict


class TTLDictTest(TestCase):
    """ TTLDict tests """
    def test_simple_no_ttl(self):
        """ Test simple usage """
        ttl_dict = TTLDict(None)
        orig_dict = {'hello': 'world', 'intval': 3}
        ttl_dict.update(orig_dict)
        self.assertEqual(sorted(orig_dict.items()), sorted(ttl_dict.items()))
