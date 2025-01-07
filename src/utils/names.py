"""
Available driver names
"""

import pandas as pd
import git

repo = git.Repo('../models', search_parent_directories=True)


women = pd.read_csv(repo.working_tree_dir + "\\src\\av_names\\imiona_k.csv")
men = pd.read_csv(repo.working_tree_dir + "\\src\\av_names\\imiona_m.csv")

names_all = pd.concat([women, men])
possible_names = names_all[names_all["LICZBA_WYSTĄPIEŃ"] > 2137]["IMIĘ_PIERWSZE"].tolist()
