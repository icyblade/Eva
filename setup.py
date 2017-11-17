from setuptools import setup

setup(
    name='eva',
    version='0.0.1',
    packages=['eva', 'eva.dataframe', 'eva.frontend', 'eva.hardware', 'eva.hotel', 'eva.model', 'eva.ota', 'eva.pms'],
    url='https://github.com/icyblade/eva',
    license='MIT',
    author='Icyblade Dai',
    author_email='icyblade.aspx@gmail.com',
    description='Project EVA',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
)
