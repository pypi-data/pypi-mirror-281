# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib import Path
from urllib.request import urlopen
from functools import cached_property

import polars as pl
import sqlalchemy as sa

from ._version import __version__
from .paths import path_sqlite

T_BASE_ORM_MODEL = T.TypeVar("T_BASE_ORM_MODEL")
T_BASE_DATA_CLASS = T.TypeVar("T_BASE_DATA_CLASS")


@dataclasses.dataclass
class BaseDataset(T.Generic[T_BASE_ORM_MODEL, T_BASE_DATA_CLASS]):
    """
    Base class for a dataset that is backed by a SQL table.

    :param name: the dataset name
    :param id_col: the primary key column name
    :param orm_model: sqlalchemy orm model
    :param orm_table: sqlalchemy table
    :param data_class: dataclasses data class
    :param engine: sqlalchemy engine
    """

    name: str = dataclasses.field()
    id_col: str = dataclasses.field()
    orm_model: T.Type[T_BASE_ORM_MODEL] = dataclasses.field()
    orm_table: sa.Table = dataclasses.field()
    data_class: T.Type[T_BASE_DATA_CLASS] = dataclasses.field()
    engine: sa.Engine = dataclasses.field()

    @cached_property
    def df(self) -> pl.DataFrame:
        """
        Read the entire dataset into a polars DataFrame. This will be cached.
        """
        with self.engine.connect() as conn:
            return pl.read_database(
                query=f"SELECT * FROM {self.orm_table.name}",
                connection=conn,
            )

    @cached_property
    def row_map(self) -> T.Dict[T.Union[int, str], T_BASE_DATA_CLASS]:
        """
        Create a dictionary mapping the primary key to the data class instance.
        """
        dct = dict()
        id_col = self.id_col
        for row in self.df.to_dicts():
            dct[row[id_col]] = self.data_class(**row)
        return dct

    def get(self, id: T.Union[int, str]) -> T.Optional[T_BASE_DATA_CLASS]:
        """
        Get a data class instance by id value.

        .. note::

            If you have concern about mutability, you can do the following:

            .. code-block:: python

                dataset = BaseDataset(...)
                data = dataset.data_class(**dataclasses.asdict(dataset.get(id=1)))

        :param id: the primary key value.
        """
        return self.row_map.get(id)

    def get_by_kvs(self, kvs: T.Dict[str, T.Any]) -> T.List[T_BASE_DATA_CLASS]:
        """
        Get a list of data class instances by key-value pairs.

        :param kvs: key-value pairs, key is the column name, value is the value to match.
        """
        stmt = sa.select(self.orm_model)
        conditions = list()
        for k, v in kvs.items():
            conditions.append(getattr(self.orm_model, k) == v)
        if conditions:
            stmt = stmt.where(sa.and_(*conditions))
        with self.engine.connect() as conn:
            results = list()
            for row in conn.execute(stmt):
                data = self.data_class(**row._asdict())
                results.append(data)
        return results


def download_sqlite(path_sqlite: Path = path_sqlite):
    """
    Download the sqlite database file from the GitHub release page.
    """
    url = f"https://github.com/MacHu-GWU/acore_df-project/releases/download/{__version__}/acore_df.sqlite"
    path_sqlite.write_bytes(urlopen(url).read())
