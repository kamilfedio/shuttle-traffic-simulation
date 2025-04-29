"""
Available driver names
"""

import pandas as pd
from typing import List
import os

class GenerateNames:
    base_path: os.path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    paths: List[str] = ["data/av_names/imiona_m.csv", "data/av_names/imiona_k.csv"]

    def __init__(self, paths: List[os.path] | None = None) -> None:
        self.names_paths = paths if paths else self.paths
        self.names_all: pd.DataFrame | None = None

    def _generate_names(self) -> List[str]:
        for path in self.names_paths:
            yield get_names_from_path(self.base_path, path)

    def get_all_names(self) -> None:
        if self.names_all is None:
            for names in self._generate_names():
                self.names_all = pd.concat([self.names_all, names])

    @property
    def possible_names(self):
        if self.names_all is None:
            self.get_all_names()
        names_to_get: pd.Series = self.names_all[self.names_all["LICZBA_WYSTĄPIEŃ"] > 2137]["IMIĘ_PIERWSZE"]
        return names_to_get.tolist()


def get_names_from_path(base_path: str, file_path: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(base_path, file_path))
