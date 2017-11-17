import os
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))

DATA = [
    {
        'id': np.random.randint(5),
        'type': 'default_type',
        'code': 'default_code',
        'timestamp': pd.Timestamp('2017-01-01') + pd.Timedelta(days=i),
        'delta': j,
        'value_1': np.random.rand() * 100,
        'value_2': np.random.rand() * 100,
    }
    for i in range(365)
    for j in range(31)
]


def test_import_data():
    from eva.dataframe import DataFrame

    with pytest.raises(AssertionError, message='Dimensions/values is not well-defined.'):
        DataFrame(DATA)
    with pytest.raises(AssertionError, message='Dimensions/values is not well-defined.'):
        DataFrame(DATA, dimensions='id', metrics='value_1')

    DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )


def test_dimension():
    from eva.dataframe import DataFrame

    df = DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )

    df.dimensions = 'id'
    assert df.dimensions == ['id']

    df.dimensions = ['id', 'type']
    assert df.dimensions == ['id', 'type']


def test_values():
    from eva.dataframe import DataFrame

    df = DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )

    df.metrics = 'value_1'
    assert df.metrics == ['value_1']

    df.metrics = ['value_2']
    assert df.metrics == ['value_2']


def test_table_view():
    from eva.dataframe import DataFrame

    df = DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )
    table_view = df.table_view

    assert set(table_view.columns) == {'id', 'type', 'code', 'timestamp', 'delta', 'value_1', 'value_2'}
    assert (table_view.index == pd.RangeIndex(len(table_view))).all()


def test_matrix_view():
    from eva.dataframe import DataFrame

    df = DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )
    matrix_view = df.matrix_view

    assert list(matrix_view.columns.names) == [None, 'id', 'type', 'code', 'delta']
    assert matrix_view.index.name == 'timestamp'
    assert set(matrix_view.columns.get_level_values(0)) == {'value_1', 'value_2'}


def test_copy():
    from eva.dataframe import DataFrame

    df = DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )

    assert isinstance(df.copy(), DataFrame)
    assert (df.copy().values == df.values).all().all()
    assert df.copy().dimensions == df.dimensions
    assert df.copy().metrics == df.metrics


def test_native_dataframe():
    import pandas as pd
    from eva.dataframe import DataFrame

    df = DataFrame(
        DATA,
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )
    native_dataframe = pd.DataFrame(DATA)

    assert (df.index == native_dataframe.index).all()
    assert (df.columns == native_dataframe.columns).all()
    assert df.shape == native_dataframe.shape
