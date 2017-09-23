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

from marshmallow_autoschema import autoschema, One, Many


def test_dump_native_types():
    obj = MyObject(my_integer=1,
                   my_string="hello",
                   my_boolean=True)

    out, errors = obj.dump()
    assert out == {
        "my_integer": 1,
        "my_string": "hello",
        "my_boolean": True,
    }


def test_load_native_types():
    obj, errors = MyObject.load({
        "my_integer": 2,
        "my_string": "world",
        "my_boolean": False,
    })

    assert obj.my_integer == 2
    assert obj.my_string == "world"
    assert obj.my_boolean is False


def test_dump_with_relations():
    obj = MyContainer(single_object=MyObject(my_integer=1),
                      list_objects=[MyObject(my_integer=2),
                                    MyObject(my_integer=3)])
    out, errors = obj.dump()
    assert out == {
        "single_object": {"my_integer": 1, "my_string": "", "my_boolean": False},
        "list_objects": [
            {"my_integer": 2, "my_string": "", "my_boolean": False},
            {"my_integer": 3, "my_string": "", "my_boolean": False},
        ],
    }


def test_load_with_relations():
    out, errors = MyContainer.load({
        "single_object": {"my_integer": 1, "my_string": "", "my_boolean": False},
        "list_objects": [
            {"my_integer": 2, "my_string": "", "my_boolean": False},
            {"my_integer": 3, "my_string": "", "my_boolean": False},
        ],
    })

    assert out.single_object.my_integer == 1
    assert out.list_objects[0].my_integer == 2
    assert out.list_objects[1].my_integer == 3


def test_default_object_from_constructor():
    obj = MyContainer(single_object=None)
    data, errors = obj.dump()
    assert data == {
        "single_object": None,
        "list_objects": [],
    }


def test_default_list_is_distinct_per_instance():
    a = MyContainer(single_object=None)
    b = MyContainer(single_object=None)
    assert a.list_objects is not b.list_objects


@autoschema
class MyObject:

    def __init__(self, *,
                 my_integer: int=0,
                 my_string: str="",
                 my_boolean: bool=False) -> None: pass


@autoschema
class MyContainer:
    def __init__(self, *,
                 single_object: One[MyObject],
                 list_objects: Many[MyObject]=None) -> None: pass
