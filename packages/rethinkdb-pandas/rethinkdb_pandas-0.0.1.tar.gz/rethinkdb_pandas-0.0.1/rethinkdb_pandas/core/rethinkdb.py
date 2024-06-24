# -*- coding: utf-8 -*-
from typing import Literal
from rethinkdb import RethinkDB
from rethinkdb.net import Connection
from .db import get_db, DBPandas
from .table import get_table, TablePandas


class RethinkDBPandas(RethinkDB):
    def __init__(self):
        super().__init__()
        
        setattr(self, "table", get_table)
        setattr(self, "db", get_db)

    def set_loop_type(self, library:Literal["asyncio", "gevent", "tornado", "trio", "twisted"] = None):
        return super().set_loop_type(library)

    def connect(self, host:str = None, port:int = None, db:str = None, auth_key:str = None, user:str = None, password:str = None, timeout = 20, ssl:str = None, url:str = None, _handshake_version = 10, **kwargs) -> Connection:
        return super().connect(host, port, db, auth_key, user, password, timeout, ssl, url, _handshake_version, **kwargs)

    # db
    def db(self, name:str, *args) -> DBPandas:
        return super().db(name, *args)

    def table(self, name:str, *args, **kwargs) -> TablePandas:
        return TablePandas(name, *args, **kwargs)
