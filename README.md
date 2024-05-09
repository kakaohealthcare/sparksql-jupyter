# sparksql-jupyter

Spark SQL magic command for Jupyter notebooks.

![Example](screenshots/example.png)

## Prerequisites
- Python >= 3.6
- PySpark >= 2.3.0
- IPython >= 7.4.0
- Jinja2 >= 3.0.0

## Install
```
pip install sparksql-jupyter
```

## Usage

### Load
```
%load_ext sparksql_jupyter
```

### Config
```
%config SparkSql.limit=<INT>
```

|Option|Default|Description|
|---|---|---|
|`SparkSql.limit`|20|The maximum number of rows to display|

### Parameter
```
%%sparksql [-c|--cache] [-e|--eager] [-v|--view VIEW] [-l|--limit LIMIT] [-j|--jinja] [variable]
<QUERY>
```

|Parameter|Description|
|---|---|
|`-c` `--cache`|Cache dataframe|
|`-e` `--eager`|Cache dataframe with eager load|
|`-v VIEW` `--view VIEW`|Create or replace temporary view|
|`-l LIMIT` `--limit LIMIT`|The maximum number of rows to display (Default: `SparkSql.limit`)|
|`variable`|Capture dataframe in a local variable|
|`-j` `--jinja`|Capture dataframe in a local variable in jinja2 template|


## Release Note

- 2024/05/09
  - stringify timestamp with timezone columns before seriealization

