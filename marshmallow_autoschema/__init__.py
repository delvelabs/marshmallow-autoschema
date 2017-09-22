from marshmallow import Schema, post_load

from .schema_factory import schema_metafactory
from .__version__ import __version__


class FactorySchema(Schema):
    """
    Schema extension to generate the model objects on load.
    """

    @post_load
    def make(self, data):
        return self.__model__(**data)


autoschema = schema_metafactory(schema_base_class=FactorySchema)

__all__ = [
    __version__,
    autoschema,
]
