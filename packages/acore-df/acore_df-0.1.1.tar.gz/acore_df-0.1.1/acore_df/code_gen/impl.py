# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as orm

import jinja2
import polars as pl

from ..paths import path_model_py_jinja2, path_model_py, path_sqlite


def to_class_name(s: str) -> str:
    """
    Convert snake case to camel case.

    Example:

        >>> to_class_name("item_template_class")
        "ItemTemplateClass"
    """
    s = s.replace("-", "_")
    parts = [part.strip().capitalize() for part in s.split("_") if part.strip()]
    return "".join(parts)


@dataclasses.dataclass
class Dataset:
    """
    Define how you want to extract dataset from excel file.

    :param tab: sheet name in excel file.
    :param include: list of column names to include. You can either specify
        `include` or `exclude`, but not both.
    :param exclude: list of column names to exclude. You can either specify
        `include` or `exclude`, but not both.
    :param mapping: map excel column name to ORM class attribute name
    :param id_col: column name that is the primary key. 注意, 这个 id 是
        mapping 之后的 id (如果有的话).
    """

    tab: str = dataclasses.field()
    include: T.Optional[T.List[str]] = dataclasses.field(default=None)
    exclude: T.Optional[T.List[str]] = dataclasses.field(default=None)
    mapping: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    id_col: str = dataclasses.field(default="id")

    def __post_init__(self):
        if (self.include is not None) and (self.exclude is not None):
            raise ValueError

    @property
    def class_name(self) -> str:
        """
        Convert snake case to camel case.

        Example:

            >>> to_class_name("item_template_class")
            "ItemTemplateClass"
        """
        return to_class_name(self.tab)


@dataclasses.dataclass
class TypeSpec:
    """
    Map from polars type to sqlalchemy type and dataclasses type.

    :param pl_type: Polars type
    :param sa_type: Sqlalchemy type
    :param dc_type: dataclasses type
    """

    pl_type: T.Any = dataclasses.field()
    sa_type: T.Any = dataclasses.field()
    dc_type: T.Any = dataclasses.field()


try:
    pl_String = pl.String
except:
    pl_String = pl.Utf8

type_spec_mapper = {
    pl.Int64: TypeSpec(pl_type=pl.Int64, sa_type=sa.Integer, dc_type="int"),
    pl.Int32: TypeSpec(pl_type=pl.Int32, sa_type=sa.Integer, dc_type="int"),
    pl.Int16: TypeSpec(pl_type=pl.Int16, sa_type=sa.Integer, dc_type="int"),
    pl.Int8: TypeSpec(pl_type=pl.Int8, sa_type=sa.Integer, dc_type="int"),
    pl_String: TypeSpec(pl_type=pl_String, sa_type=sa.String, dc_type="str"),
}

Base = orm.declarative_base()


@dataclasses.dataclass
class DatasetMetadata:
    """
    Container for dataset metadata.

    :param dataset: :class:`Dataset`
    :param df: :class:`polars.DataFrame`
    :param schema: T.Dict[str, :class`TypeSpec`]
    :param orm_class: sqlachemy ORM class
    """

    dataset: Dataset = dataclasses.field()
    df: pl.DataFrame = dataclasses.field()
    schema: T.Dict[str, TypeSpec] = dataclasses.field()
    orm_class: T.Type[Base] = dataclasses.field()
    id_col_type_spec: TypeSpec = dataclasses.field()


def load_dataset(
    path_xlsx: Path,
    dataset: Dataset,
) -> DatasetMetadata:
    """
    Load dataset dataframe from excel file, extract type spec,
    and generate ORM class definition,
    """
    # load dataframe
    df = pl.read_excel(str(path_xlsx), sheet_name=dataset.tab)
    if dataset.include:
        df = df.select(dataset.include)
    elif dataset.exclude:
        df = df.drop(dataset.exclude)
    else:
        pass
    if dataset.mapping:
        df = df.rename(mapping=dataset.mapping)
    df = df.filter(pl.col(dataset.id_col).is_not_null())

    # extract type spec
    attrs = dict()
    schema = dict()
    for col, dtype in df.schema.items():
        # print(col, dtype) # for debug only
        type_spec = type_spec_mapper[dtype]
        schema[col] = type_spec

    # generate ORM class definition
    class_name = dataset.class_name
    bases = (Base,)
    attrs["__tablename__"] = dataset.tab
    for col, type_spec in schema.items():
        if col == dataset.id_col:
            column = sa.Column(type_spec.sa_type, primary_key=True)
        else:
            column = sa.Column(type_spec.sa_type, nullable=True)
        attrs[col] = column
    orm_class = type(class_name, bases, attrs)

    # put them into container
    dataset_metadata = DatasetMetadata(
        dataset=dataset,
        df=df,
        schema=schema,
        orm_class=orm_class,
        id_col_type_spec=schema[dataset.id_col],
    )

    return dataset_metadata


def generate_code(
    path_xlsx: Path,
    dataset_list: T.List[Dataset],
    path_sqlite: Path = path_sqlite,
    path_model_py: Path = path_model_py,
):
    """
    Generate the ``model.py`` module for lookup table.

    :param path_xlsx: path to the excel file, this is the source of truth.
    :param dataset_list: list of :class:`Dataset`, define how you want to load
        data from excel file.
    :param path_sqlite: path to the sqlite database file. excel data will be stored
        in this database.
    :param path_model_py: path to the generated ORM class definition file.
    """
    path_sqlite.unlink(missing_ok=True)

    engine = sa.create_engine(f"sqlite:///{path_sqlite}")
    dataset_metadata_list = list()
    for dataset in dataset_list:
        dataset_metadata = load_dataset(path_xlsx, dataset)
        dataset_metadata_list.append(dataset_metadata)
    Base.metadata.create_all(engine)

    with orm.Session(engine) as ses:
        for dataset_metadata in dataset_metadata_list:
            for row in dataset_metadata.df.to_dicts():
                obj = dataset_metadata.orm_class(**row)
                ses.add(obj)
        ses.commit()

    template = jinja2.Template(path_model_py_jinja2.read_text())
    content = template.render(
        dataset_metadata_list=dataset_metadata_list,
    )
    path_model_py.write_text(content)
