
# arffToDataFrame

[![PyPI version](https://badge.fury.io/py/arffToDataFrame.svg)](https://badge.fury.io/py/arffToDataFrame)

## Overview

`arffToDataFrame` is a Python package that provides a simple utility to convert ARFF (Attribute-Relation File Format) files to pandas DataFrames. This is particularly useful for data scientists and machine learning practitioners who work with ARFF files and prefer the flexibility and power of pandas for data manipulation and analysis.

## Installation

You can install the package using pip:

```sh
pip install arffToDataFrame
```

## Usage

The package provides a single function `convertToDataFrame` which takes the path to an ARFF file and returns a pandas DataFrame.

### Example

```python
import arffToDataFrame as atd

# Convert ARFF file to pandas DataFrame
df = atd.convertToDataFrame('path/to/your/file.arff', contains_attributes=True)

# Display the DataFrame
print(df)
```

## Function Documentation

### `convertToDataFrame`

Converts an ARFF file to a pandas DataFrame with the ARFF file attributes as the DataFrame column titles, unless specified otherwise.

#### Parameters:

- `filename` (str): Path to the ARFF file.
- `contains_attributes` (bool): Indicates whether the ARFF file contains attribute information. Default is `True`.

#### Returns:

- `pd.DataFrame`: DataFrame containing the data from the ARFF file.

## Project Link

GitHub: [https://github.com/ammarhaider16/arff-to-dataframe](https://github.com/ammarhaider16/arff-to-dataframe)

## Author

[@ammarhaider16](https://github.com/ammarhaider16)
