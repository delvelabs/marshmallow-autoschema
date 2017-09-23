from marshmallow_autoschema import autoschema


@autoschema
class DataStructure:

    def __init__(self, *,
                 count: int) -> None: pass


def test_schema_name_is_valid():
    assert DataStructure.__schema__.__name__ == "DataStructureSchema"


def test_model_is_constructor():
    assert DataStructure == DataStructure.__schema__.__model__
