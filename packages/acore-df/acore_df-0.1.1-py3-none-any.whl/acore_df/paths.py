# -*- coding: utf-8 -*-

from pathlib import Path

dir_here = Path(__file__).absolute().parent
PACKAGE_NAME = dir_here.name

dir_project_root = dir_here.parent

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"

# ------------------------------------------------------------------------------
# Code Generator
# ------------------------------------------------------------------------------
dir_code_gen = dir_here / "code_gen"
path_model_py_jinja2 = dir_code_gen / "model.py.jinja2"

path_model_py = dir_here / "model.py"
dir_home = Path.home()
path_sqlite = dir_home / "acore_df.sqlite"
