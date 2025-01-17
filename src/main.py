from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState
from src.models.light_control_system import ControlSystem
from numpy import mean, random

from src.utils.helpful_methods import _avg_waiting_times
from src.utils.printing_methods import print_red_queue, print_queue_state

random.seed(42)

left_light_system: LightsSystem = LightsSystem.create(TrafficLightState.GREEN, 700)
left_queue: Queue = Queue.create_queue(
    left_light_system
)

right_light_system: LightsSystem = LightsSystem.create(TrafficLightState.RED, 700)
right_queue: Queue = Queue.create_queue(
    right_light_system
)

cosh1 = []
cosh2 = []


def run_cycle(queue1: Queue, queue2: Queue, new_times: tuple[float, ...] | None = None):
    if queue1.light_state:
        print('\nRIGHT')
        queue2.run(new_times)
        print_red_queue(queue2, True)
        print("LEFT")
        queue1.run(new_times)
        print_queue_state(queue1, cosh1, False)
    else:
        print("LEFT")
        queue1.run(new_times)
        print('\nRIGHT')
        queue2.run(new_times)
        print_queue_state(queue2, cosh2, True)
        print_red_queue(queue1, False)


times: tuple[float, ...] = (15, 20)
control_system = ControlSystem.create_control_system(times[0], 1)

cycle = 0
while left_queue.current_time <= 3600:
    print('-' * 150)
    cycle_title = f'CYCLE {cycle}'
    print(f'\n{cycle_title:^150}\n')
    run_cycle(left_queue, right_queue, times)

    print(f'RIGHT: {right_queue.scan_queue()}')
    print(f'LEFT: {left_queue.scan_queue()}\n')

    times = control_system.calculate_time(right_queue.scan_queue(), left_queue.scan_queue()) \
        if right_queue.light_state else control_system.calculate_time(left_queue.scan_queue(), right_queue.scan_queue())

    cycle += 1


avgs_left = _avg_waiting_times(left_queue)
avgs_right = _avg_waiting_times(right_queue)

avg_queue_length_left = mean([cell["queue"] for cell in left_queue.black_box])
avg_queue_length_right = mean([cell["queue"] for cell in right_queue.black_box])

avg_cycle_wait_left = mean([cell["cycle_wait"] for cell in left_queue.black_box if len(cell.keys()) > 1])
avg_cycle_wait_right = mean([cell["cycle_wait"] for cell in right_queue.black_box if len(cell.keys()) > 1])

print(f'\n\n{"S T A T S":^158}')
print("-" * 158)
print(f'| DIRECTION | FIRST COLOR | DRIVERS SERVED | NO-WAIT DRIVERS | AVG WAIT TIME | AVG GREEN WAIT TIME | '
      f'AVG DRIVERS BEHIND | AVG QUEUE LENGTH | AVG CYCLE WAITS |')
print('-' * 158)
print(f'| LEFT      | GREEN       | {avgs_left["drivers_served"]:<14} | {avgs_left["no_stop_drivers"]:<15} | {avgs_left["avg_waiting_times"]:<13.2f} | '
      f'{avgs_left["avg_green_waiting_times"]:<19.2f} | {avgs_left["avg_queue_length"]:<18.2f} | '
      f'{avg_queue_length_left:<16.2f} | {avg_cycle_wait_left:<15.2f} |')

print(f'| RIGHT     | RED         | {avgs_right["drivers_served"]:<14} | {avgs_right["no_stop_drivers"]:<15} | {avgs_right["avg_waiting_times"]:<13.2f} | '
      f'{avgs_right["avg_green_waiting_times"]:<19.2f} | {avgs_right["avg_queue_length"]:<18.2f} | '
      f'{avg_queue_length_right:<16.2f} | {avg_cycle_wait_right:<15.2f} |')
print('-' * 158)
