# -*- coding: utf-8 -*-

from acore_df import api


def test():
    _ = api


if __name__ == "__main__":
    from acore_df.tests import run_cov_test

    run_cov_test(__file__, "acore_df.api", preview=False)
