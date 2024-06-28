# -*- coding: utf-8 -*-

"""
我有一个 `Google Sheet <https://docs.google.com/spreadsheets/d/1XevE2tFnjCSf0paizwanCJMgmBdChunCgAp7BvqqD0M/edit?gid=2078125107#gid=2078125107>`_
里面是 azerothcore 的各种表格数据. 这个库的目的是能更轻松的使用这些数据. 为此我们就需要定义一些
ORM class, dataclass. 我觉得手动维护这些 class 是很麻烦的, 很难保持跟 Google Sheet 同步.
于是我开发了这个模块, 能够自动帮我生成这些代码.
"""
