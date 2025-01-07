"""
Lights system manager
"""

from collections import deque
import numpy as np
from typing import List
from dataclasses import dataclass

from src.models.traffic_lights import TrafficLight, TrafficLightState
from src.models.driver import Driver


@dataclass
class LightsChangesTime:
    yellow: float
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
        self.drivers_timestamps: List[float] | None = None
        self.lights_timestamps: List[float] | None = None

    def generate_driver(self) -> None:
        self.drivers: List[Driver] = [Driver.generate_driver(driver_id=i) for i in range(self.num_drivers)]
        self.drivers_timestamps = np.cumsum([driver.arrived_time for driver in self.drivers])
        for idx, timestamp in enumerate(self.drivers_timestamps):
            self.drivers[idx].arrived_time = timestamp

    def generate_lights_timestamps(self) -> None:
        times: tuple[float, float, float] = (2, 15, 20)
        lights_change_time: LightsChangesTime = LightsChangesTime(*times)



    def swap_lights(self) -> None:
        self.traffic_lights.change_state()

    def queue_drivers(self) -> None:
        pass

    def drive(self) -> None:
        pass

    @classmethod
    def create(cls, traffic_state: TrafficLightState, num_drivers: int = 0) -> "LightsSystem":
        return cls(traffic_lights=TrafficLight.create(traffic_state), num_drivers=num_drivers)
