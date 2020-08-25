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
from datetime import datetime, timezone
from enum import Enum

from marshmallow_autoschema import Many, One, autoschema


def test_dump_native_types():
    obj = MyObject(my_integer=1,
                   my_string="hello",
                   my_datetime=datetime(1918, 11, 11),
                   my_enum=MyEnum.Green,
                   my_boolean=True)

    out = obj.dump()
    assert out == {
        "my_integer": 1,
        "my_string": "hello",
        "my_boolean": True,
        "my_enum": "Green",
        "my_datetime": "1918-11-11T00:00:00",
    }


def test_load_native_types():
    obj = MyObject.load({
        "my_integer": 2,
        "my_string": "world",
        "my_boolean": False,
    })

    assert obj.my_integer == 2
    assert obj.my_string == "world"
    assert obj.my_boolean is False


# noinspection PyTypeChecker
def test_dump_with_relations():
    obj = MyContainer(
        single_object=MyObject(my_integer=1),
        list_objects=[
            MyObject(my_integer=2, my_enum=MyEnum.Magenta),
            MyObject(my_integer=3, my_boolean=True,
                     my_datetime=datetime(1666, 6, 6))],
        list_enums=[MyEnum.Blue]
    )

    out = obj.dump()
    assert out == {
        "single_object": {
            "my_integer": 1,
            "my_string": "",
            "my_boolean": False,
            "my_datetime": None,
            "my_enum": "Red"},
        "list_objects": [
            {"my_integer": 2, "my_string": "", "my_boolean": False,
             "my_enum": "Magenta", "my_datetime": None},
            {"my_integer": 3, "my_string": "", "my_boolean": True,
             "my_enum": "Red", "my_datetime": "1666-06-06T00:00:00"},
        ],
        "list_enums": ["Blue"]
    }


def test_load_with_relations():
    out = MyContainer.load({
        "single_object": {
            "my_integer": 1,
            "my_string": "",
            "my_boolean": False},
        "list_objects": [
            {"my_integer": 2, "my_string": "", "my_boolean": False,
             "my_enum": "Magenta"},
            {"my_integer": 3, "my_string": "", "my_boolean": True,
             "my_datetime": "1666-06-06T00:00:00"},
        ],
        "list_enums": ["Red", "Green"]
    })

    assert out.list_enums == [MyEnum.Red, MyEnum.Green]
    assert out.single_object.my_integer == 1
    assert out.list_objects[0].my_integer == 2
    assert out.list_objects[1].my_integer == 3
    assert out.list_objects[0].my_enum == MyEnum.Magenta
    assert out.list_objects[1].my_datetime == datetime(1666, 6, 6)


def test_default_object_from_constructor():
    obj = MyContainer(single_object=None)
    data = obj.dump()
    assert data == {
        "single_object": None,
        "list_objects": [],
        "list_enums": [],
    }


# noinspection PyTypeChecker
def test_default_list_is_distinct_per_instance():
    a = MyContainer(single_object=None)
    b = MyContainer(single_object=None)
    assert a.list_objects is not b.list_objects


# noinspection PyArgumentList
def test_with_type_inherit():
    obj = MySubObject(my_integer=1,
                      my_other_integer=2,
                      my_enum=MyEnum.Blue,
                      my_datetime=datetime(2000, 12, 12),
                      my_string="hello",
                      my_boolean=True)

    out = obj.dump()
    assert out == {
        "my_integer": 1,
        "my_other_integer": 2,
        "my_string": "hello",
        "my_datetime": "2000-12-12T00:00:00",
        "my_enum": 'Blue',
        "my_boolean": True,
    }


class MyEnum(Enum):
    Red = '#ff0000'
    Green = '#00ff00'
    Blue = '#0000ff'
    Magenta = '#ff00ff'


@autoschema
class MyObject:
    def __init__(self, *,
                 my_integer: int = 0,
                 my_string: str = "",
                 my_boolean: bool = False,
                 my_datetime: datetime = None,
                 my_enum: MyEnum = MyEnum.Red) -> None: pass


@autoschema
class MyContainer:
    def __init__(self, *,
                 single_object: One[MyObject],
                 list_objects: Many[MyObject] = None,
                 list_enums: Many[MyEnum] = None) -> None: pass


@autoschema
class MySubObject(MyObject):

    def __init__(self, *,
                 my_other_integer: int = 0) -> None:
        pass
