from marshmallow_autoschema import autoschema


@autoschema
class DataStructure:

    def __init__(self, *,
                 count: int,
                 factor: int) -> None:
        self.derived = self.count * self.factor


def test_schema_name_is_valid():
    assert DataStructure.__schema__.__name__ == "DataStructureSchema"


def test_model_is_constructor():
    assert DataStructure == DataStructure.__schema__.__model__


def test_init_body_called_after_attributes_set():
    assert 30 == DataStructure(count=5, factor=6).derived
