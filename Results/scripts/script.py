import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import os
from textstat import flesch_kincaid_grade
import nltk
from urllib.parse import urljoin
import time

# Create a comprehensive NLP text analysis project

print("Setting up NLP Text Analysis Project...")

# First, let's read the input file to understand the structure
try:
    input_df = pd.read_excel(r"C:\Users\HP\Downloads\20211030 Test Assignment\Input.xlsx")
    print("Input file columns:", input_df.columns.tolist())
    print("Number of URLs to process:", len(input_df))
    print("\nFirst few rows:")
    print(input_df.head())
except Exception as e:
    print(f"Error reading input file: {e}")
    # Let's check what files we have
    import os
    files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    print("Available Excel files:", files)