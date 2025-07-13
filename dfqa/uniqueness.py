import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

def checkUniqueness(df):

    """
    Assess uniqueness of values in each column of a pandas DataFrame.

    This function calculates the number and percentage of unique values per column,
    and provides a sample of unique values to help identify columns with low cardinality
    or potential categorical variables.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame to analyze.

    Returns
    -------
    pandas.DataFrame
        A summary DataFrame with columns:
        - 'Column': Name of the column.
        - 'Number_Unique_Value': Number of unique values in the column.
        - 'Sample_Unique_Value': A list of up to 5 unique sample values from the column.
        - 'Percentage_of_Total_Rows_(%)': Percentage of unique values relative to total rows.

    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.
    ValueError
        If the input DataFrame is empty.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'A': [1, 2, 2, 3, 3], 'B': ['x', 'y', 'y', 'y', 'z']}
    >>> df = pd.DataFrame(data)
    >>> checkUniqueness(df)
      Column  Number_Unique_Value Sample_Unique_Value  Percentage_of_Total_Rows_(%)
    0      A                   3           [1, 2, 3]                        60.0
    1      B                   3           [x, y, z]                        60.0
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas dataframe.")
    
    if df.empty:
        raise ValueError("Input dataframe cannot be empty.")
    
    total_record = df.shape[0]
    unique = [df[col].nunique() for col in df.columns]
    unique_percent = [round((u / total_record) * 100, 2) for u in unique]

    sample_unique = []
    for col in df.columns:
        uniques = df[col].unique()
        if len(uniques) < 5:
            sample_unique.append(list(uniques))
        else:
            sample_unique.append(list(uniques[:5]))

    # Fix DataFrame constructor: pass data as dict or list of lists, not separate arguments
    res_table = pd.DataFrame({
        "Column": df.columns,
        "Number_Unique_Value": unique,
        "Sample_Unique_Value": sample_unique,
        "Percentage_of_Total_Rows_(%)": unique_percent
    })
    
    return res_table


def visualizeUniqueness(df, figsize=(14,12)):

    """
    Visualize the percentage of unique values per column as a bar plot.

    Each bar represents the percentage of unique values in a column relative
    to the total number of rows. Columns with 100% uniqueness are highlighted
    and annotated as potential primary keys (PK).

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing uniqueness summary, typically the output of
        `checkUniqueness`. Must include columns:
        - 'Column'
        - 'Percentage_of_Total_Rows_(%)'

    figsize : tuple of int, optional
        Size of the figure in inches, by default (14, 12).

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib Figure object containing the uniqueness bar plot.

    Examples
    --------
    >>> summary_df = checkUniqueness(dataframe)
    >>> fig = visualizeUniqueness(summary_df)
    >>> plt.show()
    """

    unq_plot = plt.figure(figsize=figsize)
    colors = ["#E6E6FA" if x < 100 else "#000080" for x in df["Percentage_of_Total_Rows_(%)"]]
    ax = sns.barplot(data=df, x="Column", y="Percentage_of_Total_Rows_(%)", hue="Column", palette=colors, legend=False)
    plt.title("Percentage of Unique Values by Column", fontsize=16, fontweight="bold", loc="left")
    plt.xlabel(" ")
    plt.ylabel("Percentage (%)", fontsize=12)
    plt.xticks(rotation=-90, ha="right")

    for i, v in enumerate(df["Percentage_of_Total_Rows_(%)"]):
        ax.text(i, v, f"{v:.2f}%", ha="center", va="bottom")

    plt.axhline(y=100, color="r", linestyle="--", alpha=0.7)

    for i, (col, pct) in enumerate(zip(df["Column"], df["Percentage_of_Total_Rows_(%)"])):
        if pct == 100:
            plt.text(i, 102, "PK?", ha="center", va="bottom", color="green", fontweight="bold")


    legend_elements = [Line2D([0],[0], color="#E6E6FA", lw=4, label="Normal"),
                       Line2D([0],[0], color="#000080", lw=4, label="100% Unique"),
                       Line2D([0],[0], color="r", linestyle="--", label="100% Line")]
    ax.legend(handles = legend_elements, loc="upper right")

    plt.grid(alpha=0.3)
    plt.tight_layout()
    return unq_plot