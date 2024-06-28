from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='ColumnSplitFill',
    version='0.3',
    description='A Python library for splitting DataFrame columns and forward filling data.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important for Markdown to render correctly on PyPI
    author='Ashish Jaimon George',
    author_email='ashishjaimon@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',  # List all dependencies here; this example just has pandas
    ],
    entry_points={
        'console_scripts': [
            'columnsplitfill=columnsplitfill.main:main',  # Adjust according to your package structure
        ],
    },
)
