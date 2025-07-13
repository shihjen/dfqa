import pandas as pd
import numpy as np
from openpyxl import load_workbook
from datetime import datetime
import os

def getMetadata(file_path):

    """
    Extract metadata information from a CSV or Excel file.

    This function retrieves file-level metadata such as file size and last
    modified timestamp. For Excel files, it also extracts document properties
    (title, subject, creator, creation and modification dates, category) and
    basic DataFrame info (number of rows, columns, and column names). For CSV files,
    only the DataFrame info is extracted.

    Parameters
    ----------
    file_path : str
        Path to the input file. Supported formats are '.xlsx' and '.csv'.

    Returns
    -------
    dict
        A dictionary containing metadata with keys:
        - 'file_name': Base name of the file.
        - 'file_size': Size in megabytes as a string, e.g., '1.234 MB'.
        - 'last_modified': Last modification timestamp (YYYY-MM-DD HH:MM:SS).
        - 'title': Document title (Excel only; None for CSV).
        - 'subject': Document subject (Excel only; None for CSV).
        - 'creator': Document creator (Excel only; None for CSV).
        - 'created': Document creation datetime string (Excel only; None for CSV).
        - 'modified': Document last modified datetime string (Excel only; None for CSV).
        - 'category': Document category (Excel only; None for CSV).
        - 'nrows': Number of rows in the data.
        - 'ncols': Number of columns in the data.
        - 'colName': Comma-separated column names.

    Raises
    ------
    TypeError
        If the file extension is not supported.

    Examples
    --------
    >>> metadata = getMetadata("data.xlsx")
    >>> print(metadata["file_name"])
    data.xlsx
    """

    name, extension = os.path.splitext(file_path)
    metadata = {}
    if extension not in [".xlsx", ".csv"]:
        raise TypeError("Unsupported file format.")
    
    metadata["file_name"] = os.path.basename(file_path)
    metadata["file_size"] = str(round(os.path.getsize(file_path)/1000000, 3)) + " MB"
    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
    metadata["last_modified"] = last_modified.strftime("%Y-%m-%d %H:%M:%S")

    if extension.lower() == ".xlsx":
        wb = load_workbook(file_name=file_path, read_only=True)
        props = wb.properties
        metadata["title"] = props.title
        metadata["subject"] = props.subject
        metadata["creator"] = props.creator
        metadata["created"] = props.created.strftime("%Y-%m-%d %H:%M:%S")
        metadata["modified"] = props.modified.strfyime("%Y-%m-%d %H:%M:%S")
        metadata["category"] = props.category
        df = pd.read_excel(file_path, engine="openpyxl")
        metadata["nrows"] = df.shape[0]
        metadata["ncols"] = df.shape[1]
        metadata["colName"] = ", ".join(list(df.columns.values))
    else:
        metadata["title"] = None
        metadata["subject"] = None
        metadata["creator"] = None
        metadata["created"] = None
        metadata["modified"] = None
        metadata["category"] = None
        pd.read_csv(file_path, encoding="utf-8", engine="c")
        metadata["nrows"] = df.shape[0]
        metadata["ncols"] = df.shape[1]
        metadata["colName"] = ", ".join(list(df.columns.values))
    return metadata
