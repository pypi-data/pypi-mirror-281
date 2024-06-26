import arff
import pandas as pd

def convertToDataFrame(filename: str, contains_attributes: bool = True) -> pd.DataFrame:
    """
    Converts an ARFF file to a pandas DataFrame with the ARFF file attributes as the DataFrame column titles, unless specified otherwise.

    Parameters:
    filename (str): Path to the ARFF file.
    contains_attributes (bool): Indicates whether the ARFF file contains attribute information.

    Returns:
    pd.DataFrame: DataFrame containing the data from the ARFF file.
    """
    try:
        arff_data = arff.load(open(filename))
        df = pd.DataFrame(arff_data.get("data"))

        if contains_attributes:
            column_names = [attribute[0] for attribute in arff_data.get('attributes', [])]
            df.columns = column_names
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
 