import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../python-package/'))

from eva.dataframe import DataFrame

def test_init():
    from eva.model.linear_model import LinearRegression

    model = LinearRegression()

def test_fit():
    from eva.model.linear_model import LinearRegression

    data = DataFrame(
        [
            {
                'id': np.random.randint(5),
                'type': 'default_type',
                'code': 'default_code',
                'timestamp': pd.Timestamp('2017-01-01') + pd.Timedelta(days=i),
                'delta': j,
                'value_1': np.random.rand() * 100,
                'value_2': np.random.rand() * 100,
            }
            for i in range(30)
            for j in range(5)
        ],
        dimensions=['id', 'type', 'code'],
        metrics=['value_1', 'value_2'],
    )

    dataframe_x = data.matrix_view
    dataframe_x['dayofweek'] = dataframe_x.index.to_series().apply(lambda x: x.dayofweek)
    dataframe_y = pd.DataFrame({
        'y_1': np.random.rand(30) * 100,
        'y_2': np.random.rand(30) * 100,
    })

    LinearRegression().fit(dataframe_x, dataframe_y, categorial=['dayofweek'])
