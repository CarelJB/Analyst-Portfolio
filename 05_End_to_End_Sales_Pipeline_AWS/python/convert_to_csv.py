import pandas as pd
import os

# Get script directory and build paths
script_dir = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(script_dir, "..", "data_raw")
raw_folder = os.path.abspath(raw_folder)

excel_file = os.path.join(raw_folder, "Online_Retail.xlsx")
csv_file = os.path.join(raw_folder, "Online_Retail.csv")

print("Reading Excel file...")
df = pd.read_excel(excel_file)

print("Saving as CSV...")
df.to_csv(csv_file, index=False, encoding='utf-8')

print(f"CSV saved to: {csv_file}")