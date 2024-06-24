<h1 align="center">rethinkdb-pandas</h1>
<p align="center">RethinkDB Python Driver with Pandas</p>
<br><br><br>

## 🛠️ Install
- from pip
```zsh
pip install rethinkdb-pandas
```
- from git
```zsh
pip install git+https://github.com/somehitDev/rethinkdb-pandas.git
```
<br>

## 📄 Usage
- import same as `rethinkdb python driver`
```python
from rethinkdb_pandas import r
```
- connect to server same as `rethink python driver`
```python
r.connect("{host}", {port}, **kwargs)
```
- use same as `rethinkdb python driver`
  - but, sql result return as `pd.DataFrame`
  - and pass `pd.DataFrame` into `insert` function
```python
r.table("posts").insert(
    pd.read_json("https://jsonplaceholder.typicode.com/posts")
).run(con)
df_posts = r.table("posts").run(con)
print(df_posts.head())
""" print like below
   userId  id                                              title                                               body
0       1   1  sunt aut facere repellat provident occaecati e...  quia et suscipit\nsuscipit recusandae consequu...
1       1   2                                       qui est esse  est rerum tempore vitae\nsequi sint nihil repr...
2       1   3  ea molestias quasi exercitationem repellat qui...  et iusto sed quo iure\nvoluptatem occaecati om...
3       1   4                               eum et est occaecati  ullam et saepe reiciendis voluptatem adipisci\...
4       1   5                                 nesciunt quas odio  repudiandae veniam quaerat sunt sed\nalias aut...
"""
```
<br><br>

### ⚠️ for detail information, see [rethinkdb python driver](https://github.com/rethinkdb/rethinkdb-python/blob/master/README.md)
