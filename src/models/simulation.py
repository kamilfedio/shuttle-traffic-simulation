from src.models.light_control_system import ControlSystem
from src.models.lights_system import LightsSystem
from src.models.queue import Queue
from src.models.traffic_lights import TrafficLightState
from src.utils.helpful_methods import create_blackbox, get_eval_avg
from src.utils.printing_methods import print_queue_state, print_red_queue, print_simulation_summary, print_cycle_summary
from typing import Literal


class Simulation:
    def __init__(self, left_queue: Queue, right_queue: Queue, is_debugging: bool, is_training: bool,
                 times: tuple[float, float], control_system: ControlSystem) -> None:
        self.left_queue: Queue = left_queue
        self.right_queue: Queue = right_queue
        self.control_system: ControlSystem = control_system
        self.is_debugging: bool = is_debugging
        self.is_training: bool = is_training
        self.cosh1: list = []
        self.cosh2: list = []
        self.times: tuple[float, float] = times
        self.blackbox: dict[str, dict] = {}

    @classmethod
    def create(cls, num_drivers: int = 800, left_traffic_state: TrafficLightState = TrafficLightState.GREEN,
               is_debugging: bool = False, is_training: bool = False, times: tuple[float, float] = (15, 20),
               alpha: int | float = 1, left_intensity: Literal['low', 'mid', 'high'] | None = None,
               right_intensity: Literal['low', 'mid', 'high'] | None = None) -> 'Simulation':

        intensity_params: dict = {'low': 9, 'mid': 5, 'high': 4.5}
        if left_intensity:
            if left_intensity not in intensity_params:
                raise ValueError(f'Unknown left intensity: {left_intensity}')
        if right_intensity:
            if right_intensity not in intensity_params:
                raise ValueError(f'Unknown right intensity: {right_intensity}')

        left_light_system: LightsSystem = LightsSystem.create(left_traffic_state,
                                                              intensity_params[left_intensity] if left_intensity else 5,
                                                              num_drivers)
        right_light_system: LightsSystem = LightsSystem.create(
            TrafficLightState.RED if left_traffic_state.GREEN else TrafficLightState.GREEN,
            intensity_params[right_intensity] if right_intensity else 5, num_drivers)

        return cls(
            left_queue=Queue.create_queue(left_light_system),
            right_queue=Queue.create_queue(right_light_system),
            is_debugging=is_debugging,
            is_training=is_training,
            times=times,
            control_system=ControlSystem.create_control_system(times[0], alpha)
        )

    def _run_cycle(self) -> None:
        if self.left_queue.light_state:
            data_r: tuple = self.right_queue.run(self.times)
            data_l: tuple = self.left_queue.run(self.times)
            if self.is_debugging:
                print_cycle_summary(data_r, 'RIGHT')
                print_cycle_summary(data_l, 'LEFT')
                print_red_queue(self.right_queue, True)
                print_queue_state(self.left_queue, self.cosh1, False)

        else:
            data_l: tuple = self.left_queue.run(self.times)
            data_r: tuple = self.right_queue.run(self.times)

            if self.is_debugging:
                print_cycle_summary(data_l, 'LEFT',  False)
                print_cycle_summary(data_r, 'RIGHT', False)
                print_queue_state(self.right_queue, self.cosh2, True)
                print_red_queue(self.left_queue, False)

    def _simulation_summary(self) -> None:
        print_simulation_summary(self.blackbox)

    def _eval_avg(self) -> float:
        return get_eval_avg(self.blackbox)

    def _create_blackbox(self) -> None:
        self.blackbox['left_queue'].update(create_blackbox(self.left_queue, 'left'))
        self.blackbox['right_queue'].update(create_blackbox(self.right_queue, 'right'))

    def simulate(self, simulation_seconds: int = 3600) -> None | float:
        cycle: int = 0
        self.blackbox['left_queue'] = {'first_color': self.left_queue.light_system.traffic_lights.state}
        self.blackbox['right_queue'] = {'first_color': self.right_queue.light_system.traffic_lights.state}

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

        if self.is_training:
            return self._eval_avg()

    def run_simulation_x_times(self):
        pass
