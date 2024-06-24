# -*- coding: utf-8 -*-
import pandas as pd
from rethinkdb_pandas import r


con = r.connect("192.168.0.245", db = "test")

if not "posts" in r.table_list().run(con):
    r.table_create("posts").run(con)
    r.table("posts").insert(
        pd.read_json("https://jsonplaceholder.typicode.com/posts")
    ).run(con)

df_posts = r.table("posts").run(con)
print(df_posts.head())

con.close()
