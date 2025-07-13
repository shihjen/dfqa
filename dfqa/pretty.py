import pandas as pd
import numpy as np
import plotly.graph_objects as go

def ppdf(df, table_title=None):

    """
    Generate a Plotly table figure from a pandas DataFrame with formatted headers.

    This function creates a Plotly table visualization where underscores in column
    names are replaced by spaces for better readability. It supports optional
    table titles and styles the table with specific colors and fonts.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to visualize as a Plotly table.

    table_title : str, optional
        Title to display above the table. Default is None (no title).

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly Figure object containing the styled table visualization.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'first_name': ['Alice', 'Bob'], 'age': [30, 25]}
    >>> df = pd.DataFrame(data)
    >>> fig = ppdf(df, table_title="User Information")
    >>> fig.show()
    """

    modified_col = [" ".join(col.split("_")) for col in df.columns]
    fig = go.Figure(data = [go.Table(
        header = dict(values = list(modified_col),
                      fill_color = "navy",
                      align = "left",
                      font = dict(size = 14, color = "white"),
                      height = 40),
        cells = dict(values = [df[col] for col in df.columns],
                     fill_color = "lavender",
                     align = "left",
                     font = dict(size = 14),
                     height = 30,
                     format = [{"text-wrap": "wrap"}] * len(df.columns)))
                     ])
    
    fig.update_layout(
        autosize = True,
        height = 500,
        margin = dict(l=50, r=50, t=50, b=50),
        title=dict(text=table_title, font=dict(size = 18, color = "black", family = "Arial, sans-serif" ))
    )
    return fig