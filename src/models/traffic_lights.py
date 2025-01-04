"""
Traffic light model
"""

from enum import StrEnum, auto


class TrafficLightState(StrEnum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()


class TrafficLightMode(StrEnum):
    SHUTDOWN = auto()
    STARTUP = auto()


class TrafficLight:
    def __init__(
        self,
        id: int,
        state: TrafficLightState,
        mode: TrafficLightMode,
    ):
        self.id: int = id
        self.state: TrafficLightState = state
        self.mode: TrafficLightMode = mode

    def __str__(self) -> str:
        return f"TrafficLight {self.id} - {self.state}"

    @classmethod
    def create(cls, id: int, state: TrafficLightState) -> "TrafficLight":
        return cls(
            id,
            state,
            mode=(
                TrafficLightMode.STARTUP
                if state == TrafficLightState.RED
                else TrafficLightMode.SHUTDOWN
            ),
        )

    def _get_next_state_startup(self) -> None:
        match self.state:
            case TrafficLightState.RED:
                self.state = TrafficLightState.YELLOW
            case TrafficLightState.YELLOW:
                self.state = TrafficLightState.GREEN
                self.mode = TrafficLightMode.SHUTDOWN

    def _get_next_state_shutdown(self) -> None:
        match self.state:
            case TrafficLightState.GREEN:
                self.state = TrafficLightState.YELLOW
            case TrafficLightState.YELLOW:
                self.state = TrafficLightState.RED
                self.mode = TrafficLightMode.STARTUP

    def change_state(
        self,
    ) -> None:
        if self.mode == TrafficLightMode.STARTUP:
            self._get_next_state_startup()
        else:
            self._get_next_state_shutdown()
