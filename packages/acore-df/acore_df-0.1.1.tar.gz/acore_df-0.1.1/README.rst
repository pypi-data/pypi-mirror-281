
.. image:: https://readthedocs.org/projects/acore-df/badge/?version=latest
    :target: https://acore-df.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_df-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/acore_df-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_df-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_df-project

.. image:: https://img.shields.io/pypi/v/acore-df.svg
    :target: https://pypi.python.org/pypi/acore-df

.. image:: https://img.shields.io/pypi/l/acore-df.svg
    :target: https://pypi.python.org/pypi/acore-df

.. image:: https://img.shields.io/pypi/pyversions/acore-df.svg
    :target: https://pypi.python.org/pypi/acore-df

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_df-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_df-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-df.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-df.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_df-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_df-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_df-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-df#files


Welcome to ``acore_df`` Documentation
==============================================================================
.. image:: https://acore-df.readthedocs.io/en/latest/_static/acore_df-logo.png
    :target: https://acore-df.readthedocs.io/en/latest/

这个项目是为了解决在修改 Azerothcore 世界数据库, 会存在很多 ID code 到人类友好的名字的转换问题. 在以前, 为了增加代码的可维护性, 我需要定义 ID 的 Enum, 然后用 ID 取数据库中查找其他的 attribute. 而这样做很难保证数据在不断更新过程中的一致性. 于是我设计了一个新的方案. 新方案的核心是将 Google Sheet 中编写的数据作为 Ground Truth, 然后用 Python 自动生成所有的 Enum, SqlAlchemy ORM Class, Data Class 的定义的 Python 模块, 然后将数据 load 到一个 Sqlite 数据库中. 所有的 IO 都会走本地的 Sqlite 数据库, 这样会获得非常高的性能.


.. _install:

Install
------------------------------------------------------------------------------

``acore_df`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-df

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-df
