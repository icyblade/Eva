# Basic Concepts
## DataFrame
Each `DataFrame` contains four basic parts: `dimensions`, `timestamp`, `delta` and `metrics`.
`DataFrame` has two views: table view and matrix view. Matrix view is basically the pivot table of the table view.  
Matrix view is generated as follows:
```python
# df is an instance of DataFrame
df.table_view.pivot_table(
    columns=df.dimensions+['delta'], index=df.timestamp, values=df.metrics
)
```
`dimensions` and `metrics` can be serialized.
Aggregation of `DataFrame` is lazy.
## Hotel
As every hotel has a PMS, each `Hotel` has an instance of `PMS`.
## Model
`Model` applies on `Hotel`.  
`Model` contains AutoML.
## OTA
Not implemented yet.
## PMS
`PMS` is the connector between real PMS and `eva`.  
Specially, RMS+ is a `PMS`.
