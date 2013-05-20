"""
TTL dictionary

Umm... key specific TTLs?
How to give default to __init__ nicely? Maybe drop the support for *args, **kwargs -> update() passing...?
"""

from collections import MutableMapping
from threading import RLock
import time


class TTLDict(MutableMapping):
    """ Dictionary with ttl """
    def __init__(self, *args, **kwargs):
        self._default_ttl = None
        # combine to same internal store and store tuples?
        self._values = {}
        self.update(*args, **kwargs)
        self._lock = RLock()

    def __repr__(self):
        return '<TTLDict@%#08x; ttl=%r, v=%r;>' % (id(self), self._default_ttl, self._values)

    def set_default_ttl(self, ttl):
        """ Set TTL """
        self._default_ttl = ttl

    def set_ttl(self, key, ttl, now=None):
        # pass the now to all extra functions or to none at all...
        if now is None:
            now = time.time()
        with self._lock:
            _expire, value = self._values[key]
            self._values[key] = (now + ttl, value)

    def expire_in(self, key, seconds):
        pass

    def expire_at(self, key, timestamp):
        pass

    def expire_all_at(self, timestamp):
        pass

    def expire_all_in(self, timestamp):
        pass

    # extend, shorten lifes?

    def is_expired(self, key, now=None, remove=False):
        """ Check if key has expired """
        with self._lock:
            if now is None:
                now = time.time()
            expire, _value = self._values[key]
            if expire is None:
                return False
            expired = expire < now
            if expired and remove:
                self.__delitem__(key)
            return expired

    def __len__(self):
        with self._lock:
            for key in self._values.keys():
                self.is_expired(key, remove=True)
            return len(self._values)

    def __iter__(self):
        with self._lock:
            for key in self._values.keys():
                if not self.is_expired(key, remove=True):
                    yield key

    def __setitem__(self, key, value):
        with self._lock:
            if self._default_ttl is None:
                expire = None
            else:
                expire = time.time() + self._default_ttl
            self._values[key] = (expire, value)

    def __delitem__(self, key):
        with self._lock:
            del self._values[key]

    def __getitem__(self, key):
        with self._lock:
            self.is_expired(key, remove=True)
            return self._values[key]


if __name__ == '__main__':
    testdict = TTLDict()
    testdict.set_default_ttl(4)
    for i in range(10):
        testdict['key%03d' % i] = time.ctime()
        time.sleep(1)
        print len(testdict), testdict
    while len(testdict):
        print len(testdict), testdict
        time.sleep(1)

    #testdict['bogus']
