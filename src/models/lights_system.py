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
            traffic_intensity: float | int
    ) -> None:
        self.lights_change_time: LightsChangesTime | None = None
        self.traffic_lights = traffic_lights
        self.num_drivers = num_drivers
        self.drivers: List[Driver] | None = None
        self._drivers_timestamps: List[float] | None = None
        self._lights_timestamps: List[float] | None = None
        self.traffic_intensity: float | int = traffic_intensity

    def generate_drivers(self) -> None:
        self.drivers: List[Driver] = [Driver.generate_driver(driver_id=i+1, traffic_intensity=self.traffic_intensity) for i in range(self.num_drivers)]
        self.drivers_timestamps = np.cumsum([driver.arrived_time for driver in self.drivers])
        for idx, timestamp in enumerate(self.drivers_timestamps):
            self.drivers[idx].arrived_timestamp = timestamp
            self.drivers[idx].black_box = {"arrived_time": round(float(timestamp), 4)}

    def generate_lights_timestamps(self, times: tuple[float, ...] | None = None) -> None:
        if not times:
            times: tuple[float, float] = (15, 20)

        self.lights_change_time: LightsChangesTime = LightsChangesTime(green=times[0], red=times[1])

        sum_time: int = 0 if self.traffic_lights.state == TrafficLightState.RED else 5

        lights_timestamps: List[tuple[TrafficLightState, float]] = [(self.traffic_lights.state, sum_time)]
        self.swap_lights()
        while sum_time < 3700:
            sum_time += self.lights_change_time.green if self.traffic_lights.state == TrafficLightState.RED else (self.lights_change_time.red + 5)
            lights_timestamps.append((self.traffic_lights.state, sum_time))
            self.swap_lights()

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
    def create(cls, traffic_state: TrafficLightState, traffic_intensity: float | int, num_drivers: int = 0) -> "LightsSystem":
        return cls(traffic_lights=TrafficLight.create(0, traffic_state),
                   num_drivers=num_drivers,
                   traffic_intensity=traffic_intensity
                   )
