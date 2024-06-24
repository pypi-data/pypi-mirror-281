#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
import mesh.log as log
import unittest

from mesh.macro import mps, index


class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


@mps
class X:

    def __init__(self, getter) -> None:
        super().__init__()

    def getter(self):
        return self


@mps(name="x")
class Y:

    @index(0)
    def y(self) -> str:
        return '1'

    @index(5)
    def z(self) -> str:
        """
        Test z index.
        :return: z decorator value.
        """
        return '2'


class TestMacro(unittest.TestCase):

    def test_index(self):
        y = Y()
        self.invoke(y.z)
        self.invoke(y.y)
        y.z = '100'
        self.invoke(Y.z)
        self.invoke(y.z)

    @staticmethod
    def invoke(x: str):
        log.info(x)


if __name__ == '__main__':
    unittest.main()
