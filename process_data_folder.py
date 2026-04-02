import os
from pathlib import Path

import pandas as pd


def process_files(folder_path: str, extensions=(".txt",)) -> None:
    data = []

    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"Invalid folder path: {folder}")
        return

    try:
        files = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    except OSError as e:
        print(f"Error accessing folder: {e}")
        return

    for file_path in files:
        if not file_path.is_file():
            print(f"Skipped (not a file): {file_path.name}")
            continue

        if file_path.suffix.lower() not in extensions:
            print(f"Skipped: {file_path.name}")
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
            data.append([file_path.name, str(file_path), content])
            print(f"Processed: {file_path.name}")
        except UnicodeDecodeError:
            print(f"Error reading (not UTF-8): {file_path.name}")
        except OSError as e:
            print(f"Error reading {file_path.name}: {e}")

    df = pd.DataFrame(data, columns=["File Name", "File Path", "Content"])
    output_path = folder / "output.xlsx"

    try:
        df.to_excel(output_path, index=False)
        print(f"Excel file created at: {output_path}")
        print(f"Total processed files: {len(df)}")
    except Exception as e:
        print(f"Error writing Excel file: {e}")


if __name__ == "__main__":
    # Automatically use the workspace data folder as input.
    workspace_root = Path(__file__).resolve().parent
    data_folder = workspace_root / "data"
    process_files(str(data_folder))
