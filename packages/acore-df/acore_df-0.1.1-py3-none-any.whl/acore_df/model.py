# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as orm

from .paths import path_sqlite
from .dataset import BaseDataset, download_sqlite

Base = orm.declarative_base()



class ItemTemplateClass(Base):
    __tablename__ = "item_template_class"

    id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateClassData:
    id: int = dataclasses.field()
    name: T.Optional[str] = dataclasses.field(default=None)
    name_cn: T.Optional[str] = dataclasses.field(default=None)


class ItemTemplateSubclass(Base):
    __tablename__ = "item_template_subclass"

    id: orm.Mapped[str] = sa.Column(sa.String, primary_key=True)
    class_id: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, nullable=True)
    class_name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    class_name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    subclass_id: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, nullable=True)
    subclass_name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    subclass_name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    comments: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateSubclassData:
    id: str = dataclasses.field()
    class_id: T.Optional[int] = dataclasses.field(default=None)
    class_name: T.Optional[str] = dataclasses.field(default=None)
    class_name_cn: T.Optional[str] = dataclasses.field(default=None)
    subclass_id: T.Optional[int] = dataclasses.field(default=None)
    subclass_name: T.Optional[str] = dataclasses.field(default=None)
    subclass_name_cn: T.Optional[str] = dataclasses.field(default=None)
    comments: T.Optional[str] = dataclasses.field(default=None)


class ItemTemplateQuality(Base):
    __tablename__ = "item_template_quality"

    id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    color: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateQualityData:
    id: int = dataclasses.field()
    color: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    name_cn: T.Optional[str] = dataclasses.field(default=None)


class ItemTemplateBonding(Base):
    __tablename__ = "item_template_bonding"

    id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    abbr: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateBondingData:
    id: int = dataclasses.field()
    name: T.Optional[str] = dataclasses.field(default=None)
    name_cn: T.Optional[str] = dataclasses.field(default=None)
    abbr: T.Optional[str] = dataclasses.field(default=None)


class ItemTemplateAllowableClass(Base):
    __tablename__ = "item_template_allowable_class"

    id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateAllowableClassData:
    id: int = dataclasses.field()
    name: T.Optional[str] = dataclasses.field(default=None)
    name_cn: T.Optional[str] = dataclasses.field(default=None)


class ItemTemplateStatType(Base):
    __tablename__ = "item_template_stat_type"

    id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    type_name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_abbr: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_abbr_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    description: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateStatTypeData:
    id: int = dataclasses.field()
    type_name: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    name_cn: T.Optional[str] = dataclasses.field(default=None)
    name_abbr: T.Optional[str] = dataclasses.field(default=None)
    name_abbr_cn: T.Optional[str] = dataclasses.field(default=None)
    description: T.Optional[str] = dataclasses.field(default=None)


class ItemTemplateDamageType(Base):
    __tablename__ = "item_template_damage_type"

    id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name_cn: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class ItemTemplateDamageTypeData:
    id: int = dataclasses.field()
    name: T.Optional[str] = dataclasses.field(default=None)
    name_cn: T.Optional[str] = dataclasses.field(default=None)


class Factions(Base):
    __tablename__ = "factions"

    faction_id: orm.Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    sort_key: orm.Mapped[T.Optional[int]] = sa.Column(sa.Integer, nullable=True)
    expansion: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    type: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    name: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    description: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)
    reward: orm.Mapped[T.Optional[str]] = sa.Column(sa.String, nullable=True)


@dataclasses.dataclass
class FactionsData:
    faction_id: int = dataclasses.field()
    sort_key: T.Optional[int] = dataclasses.field(default=None)
    expansion: T.Optional[str] = dataclasses.field(default=None)
    type: T.Optional[str] = dataclasses.field(default=None)
    name: T.Optional[str] = dataclasses.field(default=None)
    description: T.Optional[str] = dataclasses.field(default=None)
    reward: T.Optional[str] = dataclasses.field(default=None)



dataset_mapping = {
    "item_template_class": {
        "orm_class": ItemTemplateClass,
        "data_class": ItemTemplateClassData,
        "id_col": "id",
    },
    "item_template_subclass": {
        "orm_class": ItemTemplateSubclass,
        "data_class": ItemTemplateSubclassData,
        "id_col": "id",
    },
    "item_template_quality": {
        "orm_class": ItemTemplateQuality,
        "data_class": ItemTemplateQualityData,
        "id_col": "id",
    },
    "item_template_bonding": {
        "orm_class": ItemTemplateBonding,
        "data_class": ItemTemplateBondingData,
        "id_col": "id",
    },
    "item_template_allowable_class": {
        "orm_class": ItemTemplateAllowableClass,
        "data_class": ItemTemplateAllowableClassData,
        "id_col": "id",
    },
    "item_template_stat_type": {
        "orm_class": ItemTemplateStatType,
        "data_class": ItemTemplateStatTypeData,
        "id_col": "id",
    },
    "item_template_damage_type": {
        "orm_class": ItemTemplateDamageType,
        "data_class": ItemTemplateDamageTypeData,
        "id_col": "id",
    },
    "factions": {
        "orm_class": Factions,
        "data_class": FactionsData,
        "id_col": "faction_id",
    },
}


@dataclasses.dataclass
class ItemTemplateClassDataset(
    BaseDataset[ItemTemplateClass, ItemTemplateClassData]
):
    pass

@dataclasses.dataclass
class ItemTemplateSubclassDataset(
    BaseDataset[ItemTemplateSubclass, ItemTemplateSubclassData]
):
    pass

@dataclasses.dataclass
class ItemTemplateQualityDataset(
    BaseDataset[ItemTemplateQuality, ItemTemplateQualityData]
):
    pass

@dataclasses.dataclass
class ItemTemplateBondingDataset(
    BaseDataset[ItemTemplateBonding, ItemTemplateBondingData]
):
    pass

@dataclasses.dataclass
class ItemTemplateAllowableClassDataset(
    BaseDataset[ItemTemplateAllowableClass, ItemTemplateAllowableClassData]
):
    pass

@dataclasses.dataclass
class ItemTemplateStatTypeDataset(
    BaseDataset[ItemTemplateStatType, ItemTemplateStatTypeData]
):
    pass

@dataclasses.dataclass
class ItemTemplateDamageTypeDataset(
    BaseDataset[ItemTemplateDamageType, ItemTemplateDamageTypeData]
):
    pass

@dataclasses.dataclass
class FactionsDataset(
    BaseDataset[Factions, FactionsData]
):
    pass



@dataclasses.dataclass
class Lookup:
    """
    The main API to access the acore dataframe data. Useful methods are:

    - :meth:`Lookup.${dataset_name}.get <acore_df.dataset.BaseDataset.get>`
    - :meth:`Lookup.${dataset_name}.get_by_kvs <acore_df.dataset.BaseDataset.get_by_kvs>`
    - :meth:`Lookup.${dataset_name}.df <acore_df.dataset.BaseDataset.df>`
    - :meth:`Lookup.${dataset_name}.row_map <acore_df.dataset.BaseDataset.row_map>`
    - :meth:`Lookup.${dataset_name}.name <acore_df.dataset.BaseDataset>`
    - :meth:`Lookup.${dataset_name}.id_col <acore_df.dataset.BaseDataset>`
    - :meth:`Lookup.${dataset_name}.orm_model <acore_df.dataset.BaseDataset>`
    - :meth:`Lookup.${dataset_name}.orm_table <acore_df.dataset.BaseDataset>`
    - :meth:`Lookup.${dataset_name}.data_class <acore_df.dataset.BaseDataset>`
    - :meth:`Lookup.${dataset_name}.engine <acore_df.dataset.BaseDataset>`
    """
    engine: sa.Engine = dataclasses.field()
    item_template_class: ItemTemplateClassDataset = dataclasses.field()
    item_template_subclass: ItemTemplateSubclassDataset = dataclasses.field()
    item_template_quality: ItemTemplateQualityDataset = dataclasses.field()
    item_template_bonding: ItemTemplateBondingDataset = dataclasses.field()
    item_template_allowable_class: ItemTemplateAllowableClassDataset = dataclasses.field()
    item_template_stat_type: ItemTemplateStatTypeDataset = dataclasses.field()
    item_template_damage_type: ItemTemplateDamageTypeDataset = dataclasses.field()
    factions: FactionsDataset = dataclasses.field()

    @classmethod
    def new(cls, path_sqlite: Path = path_sqlite):
        if path_sqlite.exists() is False:
            download_sqlite(path_sqlite=path_sqlite)

        engine = sa.create_engine(f"sqlite:///{path_sqlite}")
        return cls(
            engine=engine,
            item_template_class=ItemTemplateClassDataset(
                name="item_template_class",
                id_col="id",
                orm_model=ItemTemplateClass,
                orm_table=ItemTemplateClass.__table__,
                data_class=ItemTemplateClassData,
                engine=engine,
            ),
            item_template_subclass=ItemTemplateSubclassDataset(
                name="item_template_subclass",
                id_col="id",
                orm_model=ItemTemplateSubclass,
                orm_table=ItemTemplateSubclass.__table__,
                data_class=ItemTemplateSubclassData,
                engine=engine,
            ),
            item_template_quality=ItemTemplateQualityDataset(
                name="item_template_quality",
                id_col="id",
                orm_model=ItemTemplateQuality,
                orm_table=ItemTemplateQuality.__table__,
                data_class=ItemTemplateQualityData,
                engine=engine,
            ),
            item_template_bonding=ItemTemplateBondingDataset(
                name="item_template_bonding",
                id_col="id",
                orm_model=ItemTemplateBonding,
                orm_table=ItemTemplateBonding.__table__,
                data_class=ItemTemplateBondingData,
                engine=engine,
            ),
            item_template_allowable_class=ItemTemplateAllowableClassDataset(
                name="item_template_allowable_class",
                id_col="id",
                orm_model=ItemTemplateAllowableClass,
                orm_table=ItemTemplateAllowableClass.__table__,
                data_class=ItemTemplateAllowableClassData,
                engine=engine,
            ),
            item_template_stat_type=ItemTemplateStatTypeDataset(
                name="item_template_stat_type",
                id_col="id",
                orm_model=ItemTemplateStatType,
                orm_table=ItemTemplateStatType.__table__,
                data_class=ItemTemplateStatTypeData,
                engine=engine,
            ),
            item_template_damage_type=ItemTemplateDamageTypeDataset(
                name="item_template_damage_type",
                id_col="id",
                orm_model=ItemTemplateDamageType,
                orm_table=ItemTemplateDamageType.__table__,
                data_class=ItemTemplateDamageTypeData,
                engine=engine,
            ),
            factions=FactionsDataset(
                name="factions",
                id_col="faction_id",
                orm_model=Factions,
                orm_table=Factions.__table__,
                data_class=FactionsData,
                engine=engine,
            ),
        )