from setuptools import setup, find_packages

tests_require = [
    'pytest>=3.5.0',
    'pytest-flake8>=1.0.0',
]

setup(
    name='eva',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/icyblade/eva',
    license='MIT',
    author='Icyblade Dai',
    author_email='icyblade.aspx@gmail.com',
    description='Project EVA',
    install_requires=[
        'numpy>=1.13.0',
        'pandas>=0.20.0',
        'scikit-learn>=0.18.0',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
)
