import datetime

from sqlalchemy import func, Identity
from sqlalchemy.orm import mapped_column, Mapped

from .base import AlchemyBase
from .. import utils


# https://docs.sqlalchemy.org/en/20/core/defaults.html
# https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#abstract
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-type-map-pep593


class AlchemyMixin:
    pass


class HasID(AlchemyMixin):
    id: Mapped[int] = mapped_column(
        Identity(), primary_key=True, sort_order=-100
    )


class HasTimestamp(AlchemyMixin):
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), sort_order=100
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=utils.naive_utc,
        sort_order=101,
    )


class AlchemyEntity(AlchemyBase, HasID, HasTimestamp):
    __abstract__ = True


class SoftDeletable(AlchemyMixin):
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(
        sort_order=102
    )
