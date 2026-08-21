import pandas as pd
from io import StringIO


async def data_analysis(query: str, file_path: str = None, csv_data: str = None) -> str:
    if csv_data:
        try:
            df = pd.read_csv(StringIO(csv_data))
            stats = df.describe().to_string()
            return f"Data Analysis Results:\n\nShape: {df.shape}\n\nStatistics:\n{stats}"
        except Exception as e:
            return f"Error analyzing CSV data: {str(e)}"

    if file_path:
        try:
            df = pd.read_csv(file_path)
            stats = df.describe().to_string()
            return f"Data Analysis Results for {file_path}:\n\nShape: {df.shape}\n\nStatistics:\n{stats}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    return "No data source provided. Please provide csv_data or file_path."
