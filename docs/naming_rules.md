# Naming Rules

## HDFS Data
Path of HDFS data should follow this basic structure:

`hdfs://{root}/{table_name}/{l1_key}={l1_value}/{l2_key}={l2_value}/.../{ln_key}={ln_value}`

where
 - `root` is the root directory of HDFS data.
 - `table_name` is the desired table name.
 - `li_key/li_value` pairs are key and values of level `i` partition.

For example: `hdfs://data/shopping_log/type=food/date=20170101` is a valid path.

**Note**
 - `root` is fixed among every `eva` instances.
 - `table_name` should not have multiple levels, thus `hdfs://data/shopping_log/food/date=20170101` is invalid.
 - `li_key` is necessary, thus `hdfs://data/shopping_log/type=food/20170101` is invalid.