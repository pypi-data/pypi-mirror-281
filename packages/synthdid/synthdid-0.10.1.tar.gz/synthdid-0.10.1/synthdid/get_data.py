import pandas as pd, numpy as np

def california_prop99() -> pd.DataFrame:
    return pd.read_csv("https://github.com/d2cml-ai/Synthdid.jl/raw/stag_treat/data/california_prop99.csv", sep=";")

def quota() -> pd.DataFrame:
    return pd.read_csv("https://github.com/d2cml-ai/Synthdid.jl/raw/stag_treat/data/quota.csv")

# print(quota())
# _path = os.path.join(os.path.dirname(__file__), '../data/MLAB_data.txt')

# def fetch_CaliforniaSmoking() -> pd.DataFrame:
#     """
#     This data is from https://web.stanford.edu/~jhain/synthpage.html
#     [Return]
#     pd.DataFrame
#     """
    
#     _raw = pd.read_csv(_path, sep="\t", header=None)

#     _raw.columns = [
#         "Alabama",
#         "Arkansas",
#         "Colorado",
#         "Connecticut",
#         "Delaware",
#         "Georgia",
#         "Idaho",
#         "Illinois",
#         "Indiana",
#         "Iowa",
#         "Kansas",
#         "Kentucky",
#         "Louisiana",
#         "Maine",
#         "Minnesota",
#         "Mississippi",
#         "Missouri",
#         "Montana",
#         "Nebraska",
#         "Nevada",
#         "New Hampshire",
#         "New Mexico",
#         "North Carolina",
#         "North Dakota",
#         "Ohio",
#         "Oklahoma",
#         "Pennsylvania",
#         "Rhode Island",
#         "South Carolina",
#         "South Dakota",
#         "Tennessee",
#         "Texas",
#         "Utah",
#         "Vermont",
#         "Virginia",
#         "West Virginia",
#         "Wisconsin",
#         "Wyoming",
#         "California",
#     ]

#     _raw.index = [i for i in range(1962, 2001)]

#     return _raw.loc[1970:]