from setuptools import setup, find_packages

setup(
    name='ColumnSplitFill',
    version='0.1',
    description='A Python library for splitting DataFrame columns and forward filling data.',
    author='Ashish Jaimon George',
    author_email='ashishjaimon@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ]
)
