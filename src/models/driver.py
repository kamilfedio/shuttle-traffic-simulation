from typing import List
from src.utils.names import possible_names
import numpy as np
import random

"""
Driver model
"""

'''
Co on potrzebuje?
- imie
- id
- czipsy
- jesli czipsy, to generowany numer z inv U^2
- czas reakcji (Dla kazdego??), dla pierwszego moze byc dluzszy
- zbieranie danych i zeby fajnie zwracal np liste z liczbami
'''

RED_RUNNING_TIMES = np.concatenate((abs(np.random.normal(0, 1.8, 300)),
                                    abs(np.random.normal(8.5, 1.75, 200)),
                                    np.random.uniform(11, 100, 4000))).tolist()


class Driver:
    def __init__(
        self,
        driver_id: int,
        name: str,
        lays: bool,
        reaction_time: float,
        red_running_time: float = 0,
        black_box: List = []
    ):
        self.driver_id = driver_id
        self.name = name
        self.lays = lays
        self.reaction_time = reaction_time
        self.red_running_time = red_running_time
        self.black_box = black_box

    def __str__(self) -> str:
        return (f"Driver {self.driver_id}: {self.name}\n"
                f"Reaction time: {self.reaction_time}\n"
                f"Is mentally challenged: {self.lays}\n"
                f"Data collected: {self.black_box}")

    @classmethod
    def generate_driver(cls, driver_id: int) -> "Driver":
        return cls(
            driver_id,
            name=np.random.choice(possible_names),
            lays=(1 == np.random.randint(1, 51)),
            reaction_time=np.random.lognormal(-0.4, 0.38, 1) + 0.3,
            red_running_time=random.sample(RED_RUNNING_TIMES, 1)
        )

    def get_data(self):
        return self.black_box
