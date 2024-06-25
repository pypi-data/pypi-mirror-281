##  @package seal.core.misc
#   Miscellaneous useful Python extensions.

import datetime, os, pty, unicodedata, sys, imp, threading, traceback, importlib
import signal
from itertools import islice, chain
from importlib import import_module
from io import StringIO
from time import time
from math import inf
from collections.abc import Callable, MutableSequence, MutableMapping


#--  General  ------------------------------------------------------------------

##  Checks whether the object has the given type.

def check_type (x, t):
    xnames = [c.__name__ for c in x.__class__.__mro__]
    if isinstance(t, (tuple, list)):
        types = t
    else:
        types = [t]
    for ty in types:
        if isinstance(ty, str):
            name = ty
        else:
            name = ty.__name__
        if name in xnames:
            return
    raise Exception('Object does not have required type: %s, %s' % (x, t))


#--  Matching  -----------------------------------------------------------------

##  Indicates whether the object matches the description.

def matches (x, descr):
    for (k, v) in descr.items():
        if v is None: continue
        if not hasattr(x, k): return False
        val = getattr(x, k)
        if isinstance(val, Callable): val = val()
        if isinstance(v, list):
            if val not in v: return False
        else:
            if val != v: return False
    return True


##  Returns a module given its name.
#   May raise ModuleNotFoundError

def string_to_module (s):
    if not s:
        raise Exception('Require nonempty name')
    return import_module(s)

##  Takes a fully-qualified name and gets the object.

def string_to_object (s):
    j = s.rfind('.')
    if j < 0:
        raise Exception('Require fully qualified name')
    m = string_to_module(s[:j])
    return m.__dict__[s[j+1:]]


#--  Object  -------------------------------------------------------------------

class Object (object):

    def __init__ (self, *args, **kwargs):
        d = dict(kwargs)
        object.__setattr__(self, '_dict', d)
        if d:
            object.__setattr__(self, '_listlen', None)
            for (i, arg) in enumerate(args):
                d[i] = arg
        else:
            object.__setattr__(self, '_listlen', len(args))
            self.extend(args)

    def _setlistlen (self, n):
        object.__setattr__(self, '_listlen', n)

    def __getitem__ (self, key):
        return self._dict[key]

    def __getattr__ (self, name):
        return self._dict[name]
            
    def __setitem__ (self, name, value):
        self._dict[name] = value
        n = self._listlen
        if not (isinstance(name, int) and n is not None and 0 <= name < n):
            self._setlistlen(None)

    def __setattr__ (self, name, value):
        self.__setitem__(name, value)

    def append (self, value):
        if self._listlen is None:
            raise Exception('Not a list-like Object')
        else:
            n = self._listlen
            self._setlistlen(n + 1)
            self._dict[n] = value

    def extend (self, values):
        for val in values:
            self.append(val)

    def __iter__ (self):
        if self._listlen is None:
            for k in self._dict.keys():
                yield k
        else:
            for i in range(self._listlen):
                yield self._dict[i]

    def __len__ (self): return len(self._dict)
    def items (self): return self._dict.items()
    def keys (self): return self._dict.keys()
    def values (self): return self._dict.values()

    def __repr__ (self):
        if self._listlen is None:
            return repr(self._dict)
        else:
            return repr(list(self))


#--  ListProxy, MapProxy  ------------------------------------------------------

class ListProxy (MutableSequence):

    # required
    def __getitem__ (self, idx): return self.__proxyfor__.__getitem__(idx)
    def __setitem__ (self, idx, value): return self.__proxyfor__.__setitem__(idx, value)
    def __delitem__ (self, idx): return self.__proxyfor__.__delitem__(idx)
    def __len__ (self): return self.__proxyfor__.__len__()
    def insert (self, idx, value): return self.__proxyfor__.insert(idx, value)

    # mixin
    def __iter__ (self): return self.__proxyfor__.__iter__()
    def __contains__ (self, key): return self.__proxyfor__.__contains__(key)


class MapProxy (MutableMapping):

    # required
    def __getitem__ (self, key): return self.__proxyfor__.__getitem__(key)
    def __setitem__ (self, key, value): return self.__proxyfor__.__setitem__(key, value)
    def __delitem__ (self, key): return self.__proxyfor__.__delitem__(key)
    def __iter__ (self): return self.__proxyfor__.__iter__()
    def __len__ (self): return self.__proxyfor__.__len__()

    # mixin
    def __contains__ (self, key): return self.__proxyfor__.__contains__(key)
    def get (self, key, dflt=None): return self.__proxyfor__.get(key, dflt)
    def keys (self): return self.__proxyfor__.keys()
    def values (self): return self.__proxyfor__.values()
    def items (self): return self.__proxyfor__.items()
