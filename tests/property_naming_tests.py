# MIT License
#
# Copyright (c) 2017- Delve Labs Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from unittest import TestCase
from marshmallow_autoschema import autoschema_camelcase


class PropertyNamingTest(TestCase):

    def test_serialization_to_camel_case(self):
        obj = MyObject(my_integer=1, my_simple_string="test", special_case="special")
        data, errors = obj.dump()

        self.assertEqual(data, {
            "myInteger": 1,
            "mySimpleString": "test",
            "_specialCASE": "special",
        })

    def test_load_from_camelcase(self):
        obj = MyObject(my_integer=1, my_simple_string="test", special_case="special")
        data, errors = obj.dump()

        obj, errors = MyObject.load({
            "myInteger": 1,
            "mySimpleString": "test",
            "_specialCASE": "special",
        })

        self.assertEqual(obj.my_integer, 1)
        self.assertEqual(obj.my_simple_string, "test")
        self.assertEqual(obj.special_case, "special")


@autoschema_camelcase
class MyObject:
    irregular_names = {
        "special_case": "_specialCASE",
    }

    def __init__(self, *,
                 my_integer: int=0,
                 my_simple_string: str="",
                 special_case: str="") -> None: pass
