from unittest import TestCase
from marshmallow_autoschema import autoschema


class PropertySerializationTest(TestCase):

    def test_dump_native_types(self):
        obj = MyObject(my_integer=1,
                       my_string="hello",
                       my_boolean=True)

        out, errors = obj.dump()
        self.assertEqual(out, {
            "my_integer": 1,
            "my_string": "hello",
            "my_boolean": True,
        })

    def test_load_native_types(self):
        obj, errors = MyObject.load({
            "my_integer": 2,
            "my_string": "world",
            "my_boolean": False,
        })

        self.assertEqual(obj.my_integer, 2)
        self.assertEqual(obj.my_string, "world")
        self.assertFalse(obj.my_boolean)


@autoschema
class MyObject:

    def __init__(self, *,
                 my_integer: int,
                 my_string: str,
                 my_boolean: bool) -> None: pass
