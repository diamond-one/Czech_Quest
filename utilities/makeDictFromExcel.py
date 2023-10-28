
""" 
CREATE DICT FROM EXCEL USING PANDAS
"""
import sys
sys.path.append("G:/My Drive/Code/Learn_Czech")
import pandas as pd
from pprint import pprint

file_path = r"G:\My Drive\Code\Learn_Czech\content\common_1000\common_1000.xlsx"
df = pd.read_excel(file_path)

# Create a dictionary from the DataFrame
data_dict = {int(row['Number']): [row['Czech'], row['in English']] for _, row in df.iterrows()}

# Pretty-print the dictionary
pprint(data_dict)