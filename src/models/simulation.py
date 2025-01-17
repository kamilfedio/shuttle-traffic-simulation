from typing import Any

from src.models.light_control_system import ControlSystem
from src.models.lights_system import LightsSystem
from src.models.queue import Queue
from src.models.traffic_lights import TrafficLightState
from src.utils.helpful_methods import create_blackbox
from src.utils.printing_methods import print_queue_state, print_red_queue, simulation_summary


class Simulation:
    def __init__(self, left_queue: Queue, right_queue: Queue, is_debugging: bool, times: tuple[float, float],
                 control_system: ControlSystem) -> None:
        self.left_queue: Queue = left_queue
        self.right_queue: Queue = right_queue
        self.control_system: ControlSystem = control_system
        self.is_debugging: bool = is_debugging
        self.cosh1: list = []
        self.cosh2: list = []
        self.times: tuple[float, float] = times
        self.blackbox: dict[str, Any] = {}

    @classmethod
    def create(cls, num_drivers: int = 700, left_traffic_state: TrafficLightState = TrafficLightState.GREEN,
               is_debugging: bool = False, times: tuple[float, float] = (15, 20),
               alpha: int | float = 1) -> 'Simulation':
        left_light_system: LightsSystem = LightsSystem.create(left_traffic_state, num_drivers)
        right_light_system: LightsSystem = LightsSystem.create(
            TrafficLightState.RED if left_traffic_state.GREEN else TrafficLightState.GREEN, num_drivers)

        return cls(
            left_queue=Queue.create_queue(left_light_system),
            right_queue=Queue.create_queue(right_light_system),
            is_debugging=is_debugging,
            times=times,
            control_system=ControlSystem.create_control_system(times[0], alpha)
        )

    def _run_cycle(self) -> None:
        if self.left_queue.light_state:
            print('\nRIGHT')
            self.right_queue.run(self.times)
            print_red_queue(self.right_queue, True)
            print("LEFT")
            self.left_queue.run(self.times)
            print_queue_state(self.left_queue, self.cosh1, False)
        else:
            print("LEFT")
            self.left_queue.run(self.times)
            print('\nRIGHT')
            self.left_queue.run(self.times)
            print_queue_state(self.right_queue, self.cosh2, True)
            print_red_queue(self.left_queue, False)

    def _simulation_summary(self) -> None:
        simulation_summary(self.blackbox)

    def _create_blackbox(self) -> None:
        self.blackbox['left_queue'] = create_blackbox(self.left_queue, 'left')
        self.blackbox['right_queue'] = create_blackbox(self.right_queue, 'right')

    def simulate(self, simulation_seconds: int = 3600) -> None:
        cycle: int = 0
        while self.left_queue.current_time <= simulation_seconds:
            self._run_cycle()
            self.times = self.control_system.calculate_time(
                self.right_queue.scan_queue(), self.left_queue.scan_queue()) \
                if self.right_queue.light_state \
                else self.control_system.calculate_time(
                self.left_queue.scan_queue(), self.right_queue.scan_queue())

            if self.is_debugging:
                print(f'RIGHT: {self.right_queue.scan_queue()}')
                print(f'LEFT: {self.left_queue.scan_queue()}\n')

            cycle += 1

        self._create_blackbox()

        if self.is_debugging:
            self._simulation_summary()

    def run_simulation_x_times(self):
        pass
