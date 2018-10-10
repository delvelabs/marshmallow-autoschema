from marshmallow_autoschema.schema_factory import check_type, One, Many, List


def test_primitives_found():
    assert check_type(int, float, int)


def test_primitives_not_found():
    assert not check_type(str, float, int)


def test_list_of_primities():
    assert check_type(List[str], List)


def test_many_ptimities():
    assert check_type(Many[str], Many)


def test_one_subclass():
    class C:
        pass
    assert check_type(One[C], One)
