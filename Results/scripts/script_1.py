# Let's install required packages and start building the NLP project
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin
import time

print("Setting up NLP Text Analysis Project...")

# Let's first check the structure of available files
try:
    # Read input file
    input_df = pd.read_excel(r"C:\Users\HP\Downloads\20211030 Test Assignment\Input.xlsx")
    print("Input file structure:")
    print(input_df.columns.tolist())
    print(f"Number of URLs: {len(input_df)}")
    print("\nSample data:")
    print(input_df.head(3))
except Exception as e:
    print(f"Error reading input file: {e}")
    
# Check output structure
try:
    output_df = pd.read_excel('Output-Data-Structure.xlsx')
    print("\n\nOutput file structure:")
    print(output_df.columns.tolist())
    print("\nExpected columns for output:")
    for col in output_df.columns:
        print(f"- {col}")
except Exception as e:
    print(f"Error reading output structure: {e}")