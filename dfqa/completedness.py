import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def checkCompletedness(df):

    """
    Check the completeness of a pandas DataFrame by computing missing values and their percentages.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame to check for missing values.

    Returns
    -------
    pandas.DataFrame
        A summary table with the following columns:
        - 'Column': Name of the column.
        - 'Missing_Value': Number of missing (NaN) values in the column.
        - 'Missingness_Percentage_(%)': Percentage of missing values per column, rounded to two decimal places.

    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.
    ValueError
        If the input DataFrame is empty.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'A': [1, None, 3], 'B': [4, 5, None]}
    >>> df = pd.DataFrame(data)
    >>> checkCompletedness(df)
       Column  Missing_Value  Missingness_Percentage_(%)
    0       A              1                        33.33
    1       B              1                        33.33
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas dataframe.")
    
    if df.empty:
        raise ValueError("Input dataframe cannot be empty.")
    
    total_record = df.shape[0]
    missing = df.isna().sum().values
    missing_percent = [round((i/total_record)*100, 2) for i in missing]
    res_table = pd.DataFrame([df.columns, missing, missing_percent]).T
    res_table.columns = ["Column","Missing_Value","Missingness_Percentage_(%)"]
    return res_table


def visualizeCompletedness(df, figsize=(12, 7), palette="flare_r", save_path=None, dpi=300):
    
    """
    Visualize the percentage of missing values by column using a bar plot.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing the missing value summary, typically the output
        of `checkCompletedness`. It must include the columns:
        - 'Column'
        - 'Missingness_Percentage_(%)'

    figsize : tuple of int, optional
        Size of the figure in inches, by default (12, 7).

    palette : str, optional
        Color palette to use for the seaborn bar plot, by default "flare_r".

    save_path : str or None, optional
        File path to save the plot image. If None (default), the plot is not saved.

    dpi : int, optional
        Resolution in dots per inch for saving the figure, by default 300.

    Returns
    -------
    matplotlib.figure.Figure or None
        A matplotlib Figure object containing the bar plot. Returns None if the input
        DataFrame does not contain the required columns.

    Raises
    ------
    ValueError
        If required columns are missing from the input DataFrame.

    Examples
    --------
    >>> summary_df = checkCompletedness(data)
    >>> fig = visualizeCompletedness(summary_df, save_path="missingness.png")
    >>> if fig: plt.show()
    """
    required_columns = {"Column", "Missingness_Percentage_(%)"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Input DataFrame must contain the columns: {required_columns}")

    compltd_plot = plt.figure(figsize=figsize)
    ax = sns.barplot(data=df, x="Column", y="Missingness_Percentage_(%)", hue="Column", palette=palette, legend=False)

    plt.title("Percentage of Missing Values by Attribute", fontsize=14, fontweight="bold", loc="left")
    plt.ylabel("Percentage (%)")
    plt.xlabel(" ")
    plt.xticks(rotation=-90, ha="right", fontsize=9)
    plt.grid(alpha=0.4)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f%%", label_type="edge")

    plt.tight_layout()

    if save_path:
        try:
            compltd_plot.savefig(save_path, dpi=dpi)
            print(f"Plot saved to {save_path}")
        except Exception as e:
            print(f"Failed to save figure: {e}")

    return compltd_plot
