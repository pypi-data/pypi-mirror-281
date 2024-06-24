# -*- coding: utf-8 -*-
import pandas as pd
from rethinkdb.ast import (
    Table, Insert, Get, GetAll
)


def get_table(name:str, *args, **kwargs) -> "TablePandas":
    return TablePandas(name, *args, **kwargs)

class TablePandas(Table):
    def insert(self, data:pd.DataFrame | list | dict, *args, **kwargs) -> Insert:
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient = "records")
            
        return super().insert(data, *args, **kwargs)
    
    def get(self, *args) -> "GetPandas":
        return GetPandas(*args)
    
    def get_all(self, *args, **kwargs) -> "GetAllPandas":
        return GetAllPandas(*args, **kwargs)
    
    def run(self, c = None, **global_optargs) -> pd.DataFrame:
        return pd.DataFrame.from_records(super().run(c, **global_optargs).items)

class GetPandas(Get):
    def run(self, c = None, **global_optargs) -> pd.DataFrame:
        return pd.DataFrame.from_records(super().run(c, **global_optargs).items)

class GetAllPandas(GetAll):
    def run(self, c = None, **global_optargs) -> pd.DataFrame:
        return pd.DataFrame.from_records(super().run(c, **global_optargs).items)
