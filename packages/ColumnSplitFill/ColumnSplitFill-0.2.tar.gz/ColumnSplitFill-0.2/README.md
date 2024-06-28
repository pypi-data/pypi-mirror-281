
# ColumnSplitFill

ColumnSplitFill is a Python library designed for splitting DataFrame columns based on a delimiter and forward filling the data.

## Features

- Split columns based on a specified delimiter.
- Automatically forward fill other columns in the DataFrame.

## Installation

To install ColumnSplitFill, run the following command:

```bash
pip install ColumnSplitFill
```

## Usage Example

Here's how you can use the ColumnSplitFill library to manage and process your data:

```python
import pandas as pd
from ColumnSplitFill import process_data

# Example DataFrame
data = {
    'ID': [1, 2, 3],
    'Column1': ['A,B,C', 'D,E', 'F'],
    'Column2': ['Value1', 'Value4', 'Value7'],
    'Column3': ['Value2', 'Value5', 'Value8'],
    'Column4': ['Value3', 'Value6', 'Value9']
}
df = pd.DataFrame(data)

# Process the data
# Assuming 'process_data' is a function you've defined to split and fill the columns
processed_data = process_data(df, 'Column1', ',')

# Display the processed data
print(processed_data)
```
```
