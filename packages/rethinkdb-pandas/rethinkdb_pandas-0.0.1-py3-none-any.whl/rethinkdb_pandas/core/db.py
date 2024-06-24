# -*- coding: utf-8 -*-
from rethinkdb.ast import DB
from .table import TablePandas


def get_db(name:str, *args) -> "DBPandas":
    return DBPandas(name, *args)

class DBPandas(DB):
    def table(self, name:str, *args, **kwargs) -> TablePandas:
        return TablePandas(name, *args, **kwargs)
