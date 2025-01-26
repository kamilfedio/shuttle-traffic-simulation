"""
Driver model
"""

from typing import Any, List
from src.utils.names import GenerateNames
import numpy as np
import random

RED_RUNNING_TIMES: List[float] = list(np.concatenate([abs(np.random.normal(0, 1.2, 3000)),
                                    abs(np.random.normal(5, 1.2, 2000))]))
RED_RUNNING_TIMES = list(time for time in RED_RUNNING_TIMES if time < 5)

generate_names: GenerateNames = GenerateNames()


class Driver:
    """
    Co on potrzebuje?
    - imie
    - id
    - czipsy
    - jesli czipsy, to generowany numer z inv U^2
    - czas reakcji (Dla kazdego??), dla pierwszego moze byc dluzszy
    - zbieranie danych i zeby fajnie zwracal np liste z liczbami
    """

    def __init__(
            self,
            driver_id: int,
            name: str,
            lays: bool,
            reaction_time: float,
            arrived_time: float,
            red_running_time: float = 0,
    ):
        self.driver_id: int = driver_id
        self.name: str = name
        self.lays: bool = lays
        self.red_running_time: float = red_running_time
        self._reaction_time: float = reaction_time
        self._arrived_time: float = arrived_time
        self._black_box: dict = dict()
        self._arrived_timestamp: float | None = None

    def __str__(self) -> str:
        return (f"Driver {self.driver_id}: {self.name}\n"
                f"Reaction time: {self.reaction_time}\n"
                f"Is mentally challenged: {self.lays}\n"
                f"Data collected: {self.black_box}")

    @classmethod
    def generate_driver(cls, driver_id: int, traffic_intensity: float | int) -> "Driver":
        return cls(
            driver_id,
            name=np.random.choice(generate_names.possible_names),
            lays=(1 == np.random.randint(1, 51)),
            reaction_time=np.random.lognormal(-0.4, 0.38, 1).tolist()[0] + 0.3,
            red_running_time=random.sample(RED_RUNNING_TIMES, 1
                                           )[0],
            arrived_time=np.random.exponential(traffic_intensity, 1).tolist()[0] + 1
        )

    @property
    def black_box(self) -> dict:
        return self._black_box

    @black_box.setter
    def black_box(self, value: dict[str, Any]) -> None:
        for key, value in value.items():
            if isinstance(value, np.float64):
                value = round(float(value), 2)
            self._black_box[key] = value

    @property
    def reaction_time(self):
        return self._reaction_time

    @property
    def arrived_time(self):
        return self._arrived_time

    @property
    def arrived_timestamp(self):
        return self._arrived_timestamp

    @arrived_timestamp.setter
    def arrived_timestamp(self, value):
        self._arrived_timestamp = value
