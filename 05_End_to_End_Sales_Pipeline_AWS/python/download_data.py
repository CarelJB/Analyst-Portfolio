import requests
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the project folder, then into data_raw
raw_data_folder = os.path.join(script_dir, "..", "data_raw")
raw_data_folder = os.path.abspath(raw_data_folder)  # resolve to absolute path

# Create the raw data folder if it doesn't exist
os.makedirs(raw_data_folder, exist_ok=True)

# URL of the Online Retail dataset (Excel format)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
filename = os.path.join(raw_data_folder, "Online_Retail.xlsx")

print("Downloading dataset...")
response = requests.get(url, timeout=120)
response.raise_for_status()
with open(filename, "wb") as f:
    f.write(response.content)

print(f"Dataset saved to: {filename}")
