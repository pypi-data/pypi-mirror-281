# -*- coding: utf-8 -*-
"""
Unofficial Python driver library for the RethinkDB database server with Pandas
"""

__version__ = "0.0.1"

from .core.rethinkdb import RethinkDBPandas as __RethinkDBPandas
r = __RethinkDBPandas()

__all__ = [
    "r"
]
