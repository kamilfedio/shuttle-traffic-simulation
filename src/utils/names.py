"""
Available driver names
"""

import pandas as pd
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

women = pd.read_csv(os.path.join(path, "data/av_names/imiona_k.csv"))
men = pd.read_csv(os.path.join(path, "data/av_names/imiona_m.csv"))

names_all = pd.concat([women, men])
possible_names = names_all[names_all["LICZBA_WYSTĄPIEŃ"] > 2137]["IMIĘ_PIERWSZE"].tolist()
