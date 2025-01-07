"""
Lights system manager
"""

import numpy as np
from typing import List
from dataclasses import dataclass

from src.models.traffic_lights import TrafficLight, TrafficLightState
from src.models.driver import Driver


@dataclass
class LightsChangesTime:
    green: float
    red: float


class LightsSystem:
    def __init__(
            self,
            traffic_lights: TrafficLight,
            num_drivers: int,
    ) -> None:
        self.traffic_lights = traffic_lights
        self.num_drivers = num_drivers
        self.drivers: List[Driver] | None = None
        self._drivers_timestamps: List[float] | None = None
        self._lights_timestamps: List[float] | None = None

    def generate_driver(self) -> None:
        self.drivers: List[Driver] = [Driver.generate_driver(driver_id=i) for i in range(self.num_drivers)]
        self.drivers_timestamps = np.cumsum([driver.arrived_time for driver in self.drivers])
        for idx, timestamp in enumerate(self.drivers_timestamps):
            self.drivers[idx].arrived_timestamp = timestamp

    def generate_lights_timestamps(self) -> None:
        times: tuple[float, float] = (15, 20)
        lights_change_time: LightsChangesTime = LightsChangesTime(*times)
        sum_time: int = 0

        lights_timestamps: List[tuple[TrafficLightState, float]] = []
        idx = 0
        while sum_time < 3600:
            sum_time += lights_change_time.green if self.traffic_lights.state == TrafficLightState.GREEN else lights_change_time.red
            lights_timestamps.append((self.traffic_lights.state, sum_time))
            idx = 1 if idx == 0 else 0

        self._lights_timestamps = lights_timestamps

    def swap_lights(self) -> None:
        self.traffic_lights.change_state()

    def queue_drivers(self) -> None:
        pass

    def drive(self) -> None:
        pass

    @property
    def lights_timestamps(self) -> List[tuple[TrafficLightState, float]] | None:
        return self._lights_timestamps

    @lights_timestamps.setter
    def lights_timestamps(self, value: List[tuple[TrafficLightState, float]]) -> None:
        self._lights_timestamps = value

    @property
    def drivers_timestamps(self) -> List[float] | None:
        return self._drivers_timestamps

    @drivers_timestamps.setter
    def drivers_timestamps(self, value: List[float]) -> None:
        self._drivers_timestamps = value

    @classmethod
    def create(cls, traffic_state: TrafficLightState, num_drivers: int = 0) -> "LightsSystem":
        return cls(traffic_lights=TrafficLight.create(0, traffic_state), num_drivers=num_drivers)
