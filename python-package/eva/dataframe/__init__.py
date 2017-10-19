import pandas as pd
from eva.hardware import cpu, io


class DataFrame(pd.DataFrame):
    # _pivot_attributes = {}  # member of class rather than instance, thus it will be shared among all instances

    @io
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False,
                 dimensions=None, metrics=None):
        super(DataFrame, self).__init__(data=data, index=index, columns=columns, dtype=dtype, copy=copy)

        self._pivot_attributes = {'dimensions': [], 'metrics': []}
        self.dimensions = dimensions
        self.metrics = metrics
        self._verify_integrality()

    def _verify_integrality(self):
        """Verify integrality of the DataFrame."""

        # columns should be `dimensions`, `timestamp`, `delta`, `values`
        assert 'timestamp' in self.columns, '`timestamp` not found.'
        assert 'delta' in self.columns, '`delta` not found.'
        assert set(self.dimensions + self.metrics + ['timestamp', 'delta']) == set(self.columns.tolist()), (
            'Dimensions/values is not well-defined.'
        )

        # index should be native
        assert (self.index == pd.RangeIndex(len(self))).all()

    @property
    def dimensions(self):
        return self._pivot_attributes['dimensions']

    @dimensions.setter
    def dimensions(self, dimensions):
        if dimensions is None:
            dimensions = []
        elif not isinstance(dimensions, list):
            dimensions = [dimensions]
        self._pivot_attributes['dimensions'] = dimensions

    @property
    def metrics(self):
        return self._pivot_attributes['metrics']

    @metrics.setter
    def metrics(self, metrics):
        if metrics is None:
            metrics = []
        elif not isinstance(metrics, list):
            metrics = [metrics]
        self._pivot_attributes['metrics'] = metrics

    @property
    def table_view(self):
        return self

    @property
    @cpu
    def matrix_view(self, fill_value=None):
        # TODO: matrix_view should be an instance of eva.dataframe.DataFrame rather than pandas.DataFrame
        return self.pivot_table(
            index='timestamp',
            columns=self.dimensions + ['delta'],
            values=self.metrics,
            fill_value=fill_value
        )

    def copy(self, deep=True):
        df = super(DataFrame, self).copy(deep)
        return DataFrame(df, dimensions=self.dimensions, metrics=self.metrics)

    def _pk2bk(self):
        raise NotImplementedError

    def _bk2pk(self):
        raise NotImplementedError
