from pathlib import Path
import pandas as pd

def create_sample_excel_files(sample_data_folder):
    """
    Generates sample Excel files with mock data.
    """
    for i in range(1, 4):
        df = pd.DataFrame({
            'ID': [i * 100 + j for j in range(1, 6)],
            'Name': [f'Product_{i}_{j}' for j in range(1, 6)],
            'Description': [f'Description for Product_{i}_{j}' for j in range(1, 6)],
            'Price': [round(10 + i * 0.5 + j * 0.1, 2) for j in range(1, 6)]
        })
        file_path = sample_data_folder / f'sample_data_{i}.xlsx'
        df.to_excel(file_path, index=False)
        print(f'Created sample Excel file: {file_path}')
