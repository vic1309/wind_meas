"""
This is the file for the sonic data.
"""

__author__ = "Astrid Myren, UiB"
__email__ = "astrid.myren@student.uib.no"

# Import pandas
import pandas as pd


# Load csv
df = pd.read_csv("Sonic_processed_2019_11_04.csv")
print(df)
