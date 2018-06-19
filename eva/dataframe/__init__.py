import pandas as pd

from eva.hardware import cpu, io


class DataFrame(object):
    @io
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False,
                 dimensions=None, metrics=None):
        self._dimensions = None
        self._metrics = None

        self._native_dataframe = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self.dimensions = dimensions
        self.metrics = metrics
        self._verify_integrality()

    def __len__(self):
        return len(self._native_dataframe)

    @property
    def index(self):
        return self._native_dataframe.index

    @property
    def columns(self):
        return self._native_dataframe.columns

    @property
    def values(self):
        return self._native_dataframe.values

    @property
    def shape(self):
        return self._native_dataframe.shape

    def _verify_integrality(self):
        """Verify integrality of the DataFrame."""

        # columns should be `dimensions`, `timestamp`, `delta`, `values`
        assert 'timestamp' in self.columns, '`timestamp` not found.'
        assert 'delta' in self.columns, '`delta` not found.'
        assert set(self.dimensions + self.metrics + ['timestamp', 'delta']) == set(self.columns.tolist()), (
            'Dimensions/values is not well-defined.'
        )
        assert not set(self.dimensions).intersection(set(self.metrics)), (
            'Duplicate feature found in dimensions and values.'
        )

        # index should be native
        assert isinstance(self.index, pd.core.index.NumericIndex)

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        if dimensions is None:
            dimensions = []
        elif not isinstance(dimensions, list):
            dimensions = [dimensions]
        self._dimensions = dimensions

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        if metrics is None:
            metrics = []
        elif not isinstance(metrics, list):
            metrics = [metrics]
        self._metrics = metrics

    @property
    def table_view(self):
        return self

    @property
    @cpu
    def matrix_view(self, fill_value=None):
        # TODO: matrix_view should be an instance of eva.dataframe.DataFrame rather than pandas.DataFrame
        return self._native_dataframe.pivot_table(
            index='timestamp',
            columns=self.dimensions + ['delta'],
            values=self.metrics,
            fill_value=fill_value
        )

    def copy(self, deep=True):
        return DataFrame(
            self._native_dataframe.copy(deep=deep),
            dimensions=self.dimensions, metrics=self.metrics
        )

    def _pk2bk(self):
        raise NotImplementedError

    def _bk2pk(self):
        raise NotImplementedError
