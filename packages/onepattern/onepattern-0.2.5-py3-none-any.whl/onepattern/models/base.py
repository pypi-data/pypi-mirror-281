from enum import Enum
from typing import Any, Self

from sqlalchemy import BigInteger, Enum as SAEnum, MetaData
from sqlalchemy.orm import (
    DeclarativeBase as SABase,
)

from onepattern import utils
from onepattern.types import ModelData

type_map = {int: BigInteger, Enum: SAEnum(Enum, native_enum=False)}

NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)


class AlchemyBase(SABase):
    type_annotation_map = type_map
    metadata = metadata

    def dump(self) -> dict[str, Any]:
        return utils.instance_dump(self)

    def update(self, update_data: ModelData) -> Self:
        return utils.update_attrs(self, update_data)
