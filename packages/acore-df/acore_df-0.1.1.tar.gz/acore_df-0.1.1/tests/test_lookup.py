# -*- coding: utf-8 -*-

import random
import dataclasses
import sqlalchemy as sa
from acore_df.model import dataset_mapping, Lookup


def test():
    lookup = Lookup.new()

    for dataset_name, dct in dataset_mapping.items():
        id_col = dct["id_col"]
        orm_class = dct["orm_class"]
        data_class = dct["data_class"]
        # print(dataset_name)
        dataset = getattr(lookup, dataset_name)

        random_id = random.choice(list(dataset.row_map.keys()))
        random_row = random.choice(list(dataset.row_map.values()))
        row_keys = list(dataclasses.asdict(random_row).keys())
        random_key = random.choice(row_keys)
        random_value = getattr(random_row, random_key)

        assert getattr(dataset.get(random_id), id_col) == random_id

        results = dataset.get_by_kvs(kvs={random_key: random_value})
        value_set = set([getattr(row, random_key) for row in results])
        assert random_value in value_set

        with lookup.engine.connect() as conn:
            stmt = sa.select(dataset.orm_table).limit(10)
            _ = list(conn.execute(stmt))


if __name__ == "__main__":
    from acore_df.tests import run_cov_test

    run_cov_test(__file__, "acore_df.model", preview=False)
