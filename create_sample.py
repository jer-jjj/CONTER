# -*- coding: utf-8 -*-
"""
Example: Create an Excel template file
Running this script will generate a sample Excel file in the current directory
"""
import pandas as pd
import os


def create_sample_excel():
    """Create sample Excel file"""
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry'],
        'ID': ['2024001', '2024002', '2024003', '2024004', '2024005', '2024006', '2024007', '2024008'],
        'Weight': [1.0, 1.0, 1.5, 1.0, 0.8, 1.0, 1.2, 1.0]
    }
    
    df = pd.DataFrame(data)
    file_path = os.path.join(os.getcwd(), 'sample_students.xlsx')
    df.to_excel(file_path, index=False)
    print(f"Sample Excel file created: {file_path}")
    return file_path


if __name__ == "__main__":
    create_sample_excel()
