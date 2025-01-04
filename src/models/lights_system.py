"""
Lights system manager
"""

from collections import deque

from src.models.traffic_lights import TrafficLight, TrafficLightState


class LightsSystem:
    def __init__(
        self,
        traffic_lights: TrafficLight,
        traffic_drivers_queue: deque | None = None,
    ) -> None:
        self.traffic_lights = traffic_lights
        self.traffic_drivers_queue = traffic_drivers_queue

    def _generate_driver(self) -> None:
        pass

    def _swap_lights(self) -> None:
        self.traffic_lights.change_state()

    def _drive(self) -> None:
        pass

    @classmethod
    def create(cls, traffic_state: TrafficLightState) -> "LightsSystem":
        return cls(TrafficLight.create(traffic_state))
