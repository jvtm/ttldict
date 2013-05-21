"""
Unit tests for TTLDict
"""

from unittest import TestCase
from ttldict import TTLDict
import time


class TTLDictTest(TestCase):
    """ TTLDict tests """
    def test_update_no_ttl(self):
        """ Test update() call """
        ttl_dict = TTLDict(None)
        orig_dict = {'hello': 'world', 'intval': 3}
        ttl_dict.update(orig_dict)
        self.assertEqual(sorted(orig_dict.items()), sorted(ttl_dict.items()))

    def test_len_clears_expired_items(self):
        """ Test that calling len() removes expired items """
        ttl_dict = TTLDict(-1, a=1, b=2)
        self.assertEqual(ttl_dict._values.keys(), sorted(['a', 'b']))
        self.assertEqual(len(ttl_dict), 0)
        self.assertEqual(ttl_dict._values.keys(), [])

    def test_expire_at(self):
        """ Test expire_at """
        ttl_dict = TTLDict(60)
        ttl_dict['a'] = 100
        ttl_dict['b'] = 123
        self.assertEqual(ttl_dict['a'], 100)
        self.assertEqual(ttl_dict['b'], 123)
        self.assertEqual(len(ttl_dict), 2)
        ttl_dict.expire_at('a', time.time())
        self.assertRaises(KeyError, lambda: ttl_dict['a'])
        self.assertEqual(len(ttl_dict), 1)
        self.assertEqual(ttl_dict['b'], 123)

    def test_set_ttl_get_ttl(self):
        """ Test set_ttl() and get_ttl() """
        ttl_dict = TTLDict(120, foo=3, bar=None)
        self.assertEqual(sorted(ttl_dict), ['bar', 'foo'])
        self.assertEqual(ttl_dict['foo'], 3)
        self.assertEqual(ttl_dict['bar'], None)
        self.assertEqual(len(ttl_dict), 2)
        ttl_dict.set_ttl('foo', 3)
        ttl_foo = ttl_dict.get_ttl('foo')
        self.assertTrue(ttl_foo <= 3.0)
        ttl_bar = ttl_dict.get_ttl('bar')
        self.assertTrue(ttl_bar - ttl_foo > 100)

    def test_set_ttl_key_error(self):
        """ Test that set_ttl() raises KeyError """
        ttl_dict = TTLDict(60)
        self.assertRaises(KeyError, ttl_dict.set_ttl, 'missing', 10)

    def test_get_ttl_key_error(self):
        """ Test that get_ttl() raises KeyError """
        ttl_dict = TTLDict(60)
        self.assertRaises(KeyError, ttl_dict.get_ttl, 'missing')

    def test_iter_empty(self):
        """ Test that empty TTLDict can be iterated """
        ttl_dict = TTLDict(60)
        for key in ttl_dict:
            self.fail("Iterating empty dictionary gave a key %r" % (key,))

    def test_iter(self):
        """ Test that TTLDict can be iterated """
        ttl_dict = TTLDict(60)
        ttl_dict.update(zip(range(10), range(10)))
        self.assertEqual(len(ttl_dict), 10)
        for key in ttl_dict:
            self.assertEqual(key, ttl_dict[key])

    def test_is_expired(self):
        """ Test is_expired() call """
        now = time.time()
        ttl_dict = TTLDict(60, a=1, b=2)
        self.assertFalse(ttl_dict.is_expired('a'))
        self.assertFalse(ttl_dict.is_expired('a', now=now))
        self.assertTrue(ttl_dict.is_expired('a', now=now+61))

        # remove=False, so nothing should be gone
        self.assertEqual(len(ttl_dict), 2)
