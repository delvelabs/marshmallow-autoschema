from marshmallow_autoschema import schema_metafactory
from marshmallow.fields import Url


class URL:
    pass


custom = schema_metafactory(extended_field_map={
    URL: Url,
})


@custom
class A:
    def __init__(self, *,
                 target: URL) -> None: pass


def test_custom_field():
    a = A(target="http://example.com/")

    data, errors = a.dump()
    assert data == {"target": "http://example.com/"}


def test_custom_field_fails_validation():
    a = A(target="example.com/")

    data, errors = a.dump(strict=False)
    assert errors == {"target": ["Not a valid URL."]}
