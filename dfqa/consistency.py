import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import re

def checkConsistency(df):

    """
    Check data type consistency for each column in a pandas DataFrame.

    This function examines each column to determine the number and types of Python
    data types present (e.g., int, float, str). It is useful for identifying columns
    with mixed types, which may indicate data quality issues.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame to check for data type consistency.

    Returns
    -------
    pandas.DataFrame
        A summary table with the following columns:
        - 'Column': Name of the column.
        - 'Number_Data_Type': Number of unique Python data types found in the column.
        - 'List_Data_Type': List of data types (as strings) present in the column.

    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.
    ValueError
        If the input DataFrame is empty.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'A': [1, 2, '3'],
    ...     'B': [4.0, 5.2, 6.1],
    ...     'C': ['x', 'y', 'z']
    ... })
    >>> checkConsistency(df)
      Column  Number_Data_Type    List_Data_Type
    0       A                  2       int, str
    1       B                  1           float
    2       C                  1             str
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas dataframe.")
    
    if df.empty:
        raise ValueError("Input dataframe cannot be empty.")
    
    dtype_num = [df[col].apply(type).nunique() for col in df.columns]
    dtype_lst = []
    for col in df.columns:
        dtype = df[col].apply(type).unique()
        dtype_lst.append(", ".join([d.__name__ for d in dtype]))
    res_table = pd.DataFrame([df.columns, dtype_num, dtype_lst]).T
    res_table.columns = ["Column", "Number_Data_Type", "List_Data_Type"]
    return res_table

def visualizeConsistency(df, figsize=(14,8), palette="flare_r"):

    """
    Visualize data type consistency across columns using a bar plot.

    This function generates a bar plot where each bar represents the number of distinct
    Python data types found in each column of a DataFrame. It helps identify columns with
    mixed data types, which could indicate data quality issues.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing the data type consistency summary, typically the output
        from `checkConsistency`. It must contain the following columns:
        - 'Column': Column name
        - 'Number_Data_Type': Number of distinct data types in the column
        - 'List_Data_Type': String representation of the data types found

    figsize : tuple of int, optional
        Size of the figure in inches, by default (14, 8).

    palette : str, optional
        Seaborn color palette used for the bar plot, by default "flare_r".

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib Figure object containing the consistency bar plot.

    Examples
    --------
    >>> summary_df = checkConsistency(dataframe)
    >>> fig = visualizeConsistency(summary_df)
    >>> plt.show()
    """

    con_plot = plt.figure(figsize=figsize)
    ax = sns.barplot(data=df, x="Column", y="Number_Data_Type", hue="Column", palette=palette, legend=False)
    plt.title("Data Type Consistency Across Columns", fontsize=16, fontweight="bold", loc="left")
    plt.xlabel(" ")
    plt.xticks(rotation=-90, ha="right")
    plt.ylabel("Number of Distinct Data Types", fontsize=12)
    ax.set_yticklabels([])

    for i, v in enumerate(df["Number_Data_Type"]):
        ax.text(i, v, str(v), ha="center", va="bottom")

    for i, (cl, num_types, type_list) in enumerate(zip(df["Column"],
                                                       df["Number_Data_Type"],
                                                       df["List_Data_Type"])):
        ax.text(i, 0.22, type_list, ha="center", va="bottom", rotation=00,
                fontsize=8, color="white", fontweight="bold")
        
    plt.axhline(y=1, color="r", linestyle="--", alpha=0.7)
    legend_elements = [Line2D([0],[0], color="r", linestyle="--", label="Ideal (1 data type)")]
    ax.legend(handles=legend_elements, loc="upper right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return con_plot

def verifyConsistency(df):

    """
    Detect potential data inconsistencies in a DataFrame, including:
    - Inconsistent date formats
    - Inconsistent boolean representations
    - String-based missing value placeholders
    - Numeric precision issues
    - Encoding anomalies

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to check for inconsistencies.

    Returns
    -------
    pandas.DataFrame
        A DataFrame listing columns and their detected inconsistencies.
    """

    inconsistencies = {}

    for col in df.columns:
        column_inconsistencies = []

        # 1. Object (string-like) column checks
        if df[col].dtype == "object":
            values = df[col].dropna()

            # a. Inconsistent date formats
            parsed_formats = set()
            for value in values:
                try:
                    parsed_date = pd.to_datetime(value, errors="raise")
                    parsed_formats.add(parsed_date.strftime("%Y-%m-%d"))
                except:
                    continue
            if len(parsed_formats) > 1:
                column_inconsistencies.append(f"Inconsistent date formats: {parsed_formats}")

            # b. Inconsistent boolean representations
            unique_vals = set(values.unique())
            boolean_aliases = {
                "TRUE", "FALSE", "True", "False", "T", "F", "t", "f",
                "YES", "NO", "Yes", "No", "Y", "N", "y", "n",
                1, 0, 1.0, 0.0
            }
            if unique_vals & boolean_aliases:
                column_inconsistencies.append(f"Possible inconsistent boolean values: {unique_vals}")

            # c. String-based missing values
            known_missing = {"NA", "N/A", "null", "none", "None", "-", "", "missing"}
            found_missing = unique_vals & known_missing
            if len(found_missing) > 0:
                column_inconsistencies.append(f"Missing value placeholders: {found_missing}")

            # d. Encoding check (basic)
            suspect_chars = values.astype(str).apply(lambda x: bool(re.search(r"[^\x00-\x7F]", x)))
            if suspect_chars.any():
                column_inconsistencies.append("Non-ASCII or encoding anomalies detected")

        # 2. Numeric precision check
        if pd.api.types.is_numeric_dtype(df[col]):
            types_in_col = df[col].dropna().apply(lambda x: type(x)).unique()
            if len(types_in_col) > 1:
                type_names = [t.__name__ for t in types_in_col]
                column_inconsistencies.append(f"Mixed numeric types: {type_names}")
            elif df[col].dropna().apply(float.is_integer).nunique() > 1:
                column_inconsistencies.append("Inconsistent numeric precision (int vs float)")

        # 3. Record inconsistencies
        if column_inconsistencies:
            inconsistencies[col] = column_inconsistencies

    # Compile result
    if not inconsistencies:
        result = pd.DataFrame(columns=["Column", "Inconsistencies"])
    else:
        result = pd.DataFrame.from_dict(inconsistencies, orient="index").reset_index()
        result.columns = ["Column", "Inconsistencies"]
    return result
