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

from marshmallow_autoschema import autoschema_camelcase, schema_metafactory


def test_serialization_to_camel_case():
    obj = MyObject(my_integer=1, my_simple_string="test", special_case="special")
    data = obj.dump()

    assert data == {
        "myInteger": 1,
        "mySimpleString": "test",
        "_specialCASE": "special",
    }


def test_load_from_camelcase():
    obj = MyObject(my_integer=1, my_simple_string="test", special_case="special")
    data = obj.dump()

    obj = MyObject.load({
        "myInteger": 1,
        "mySimpleString": "test",
        "_specialCASE": "special",
    })

    assert obj.my_integer == 1
    assert obj.my_simple_string == "test"
    assert obj.special_case == "special"


def test_custom_naming():
    @schema_metafactory(field_namer=lambda x: x.upper())
    class Custom:
        def __init__(self, *,
                     hello: int,
                     world: int) -> None: pass

    assert {"HELLO": 1, "WORLD": 2} == Custom(hello=1, world=2).dump()


@autoschema_camelcase
class MyObject:
    irregular_names = {
        "special_case": "_specialCASE",
    }

    def __init__(self, *,
                 my_integer: int=0,
                 my_simple_string: str="",
                 special_case: str="") -> None: pass
