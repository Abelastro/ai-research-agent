import os
import pandas as pd
from io import StringIO


async def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return f"File: {file_path}\n\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def read_csv(file_path: str) -> str:
    try:
        df = pd.read_csv(file_path)
        stats = df.describe().to_string()
        return f"CSV File: {file_path}\n\nShape: {df.shape}\n\nColumns: {', '.join(df.columns)}\n\nStatistics:\n{stats}"
    except Exception as e:
        return f"Error reading CSV: {str(e)}"


async def list_directory(dir_path: str) -> str:
    try:
        entries = os.listdir(dir_path)
        dirs = [e for e in entries if os.path.isdir(os.path.join(dir_path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(dir_path, e))]

        output = f"Directory: {dir_path}\n\n"
        if dirs:
            output += f"Directories ({len(dirs)}):\n"
            for d in sorted(dirs):
                output += f"  {d}/\n"
            output += "\n"
        if files:
            output += f"Files ({len(files)}):\n"
            for f in sorted(files):
                size = os.path.getsize(os.path.join(dir_path, f))
                output += f"  {f} ({size} bytes)\n"
        return output.strip()
    except Exception as e:
        return f"Error listing directory: {str(e)}"
