"""
Traffic light model
"""

from enum import StrEnum, auto


class TrafficLightState(StrEnum):
    RED = auto()
    GREEN = auto()


class TrafficLight:
    def __init__(
            self,
            traffic_id: int,
            state: TrafficLightState,
    ):
        self.traffic_id: int = traffic_id
        self._state: TrafficLightState = state

    def __str__(self) -> str:
        return f"TrafficLight {self.traffic_id} - {self.state}"

    @classmethod
    def create(cls, traffic_id: int, state: TrafficLightState) -> "TrafficLight":
        return cls(
            traffic_id,
            state,

        )

    @property
    def state(self) -> TrafficLightState:
        return self._state

    @state.setter
    def state(self, value: TrafficLightState) -> None:
        self._state = value

    def change_state(
            self,
    ) -> None:
        if self.state == TrafficLightState.RED:
            self.state = TrafficLightState.GREEN
        else:
            self.state = TrafficLightState.RED
