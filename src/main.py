from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState
from typing import List
from src.models.light_control_system import ControlSystem

left_light_system: LightsSystem = LightsSystem.create(TrafficLightState.GREEN, 500)
left_queue: Queue = Queue.create_queue(
    left_light_system
)

right_light_system: LightsSystem = LightsSystem.create(TrafficLightState.RED, 500)
right_queue: Queue = Queue.create_queue(
    right_light_system
)


def print_queue_state(queue: Queue, cosh: List, is_right: bool):
    print()
    if is_right:
        print(f' {"~ " * 25}{"R I G H T "}{"~ " * 25}~')
    else:
        print(f' {"~ " * 26}{"L E F T "}{"~ " * 25}~')
    print('-' * 112)
    print(f'| {"STATUS":<7} | {"ID":<3} | {"Driver Name":<13} | {"Arrived Time [s]":<17}' +
          f' | {"Waiting Time [s]":<17} | {"Moved Time [s]":<17} | {"Drivers in Queue":<13} |')
    print('-' * 112)

    drivers_to_show = [driver for driver in queue.happy_drivers if driver not in cosh]
    for driver in drivers_to_show:
        print(f'| RUNNING'
              f' | {str(driver.driver_id).zfill(3)}'
              f' | {driver.name:<13}'
              f' | {driver.black_box.get("arrived_time", ""):<17}'
              f' | {driver.black_box.get("waiting_time", ""):<17}'
              f' | {driver.black_box.get("moved_time", ""):<17}'
              f' | {driver.black_box.get("drivers_in_queue", ""):<16} |')
        cosh.append(driver)
    if not drivers_to_show:
        print("| Running |")
    print('-' * 112)

    print()


def print_red_queue(queue: Queue, is_right: bool):
    print()
    if is_right:
        print(f'{"~ " * 11}{"R I G H T "}{"~ " * 10}~')
    else:
        print(f'{"~ " * 11}{"L E F T "}{"~ " * 11}~')
    print('-' * 53)
    print(f'| {"STATUS":<7} | {"ID":<3} | {"Driver Name":<13} | {"Arrived Time [s]":<17} |')
    print('-' * 53)
    if not queue.cars:
        print('| WAITING |')
    for driver in queue.cars:
        print(f'| WAITING'
              f' | {str(driver.driver_id).zfill(3)}'
              f' | {driver.name:<13}'
              f' | {driver.black_box.get("arrived_time", ""):<17} |')
    print('-' * 53)
    print()


def _avg_waiting_times(queue: Queue):
    waiting_times = [happy_driver.black_box.get('waiting_time', 0) for happy_driver in queue.happy_drivers]
    queue_length = [happy_driver.black_box.get('drivers_in_queue', 0) for happy_driver in queue.happy_drivers]
    return {'avg_waiting_times': sum(waiting_times)/len(waiting_times), 'avg_queue_length': sum(queue_length)/len(queue_length)}


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

for cycle in range(100):
    print('-' * 112)
    cycle_title = f'CYCLE {cycle}'
    print(f'\n{cycle_title:^112}\n')
    run_cycle(left_queue, right_queue, times)

    print(f'RIGHT: {right_queue.scan_queue()}')
    #print(right_queue.black_box)
    print(f'LEFT: {left_queue.scan_queue()}')
    #print(left_queue.black_box)

    times = control_system.calculate_time(right_queue.scan_queue(), left_queue.scan_queue()) \
        if right_queue.light_state else control_system.calculate_time(left_queue.scan_queue(), right_queue.scan_queue())

    # print(times)

avgs_left = _avg_waiting_times(left_queue)
avgs_right = _avg_waiting_times(right_queue)

print(f'| DIRECTION | FIRST COLOR | AVG WAITING TIME | AVG LENGTH |')
print('-' * 112)
print(f'| LEFT      | GREEN       | {avgs_left["avg_waiting_times"]:<16.2f} | {avgs_left["avg_queue_length"]:<10.2f} |')
print(f'| LEFT      | RED         | {avgs_right["avg_waiting_times"]:<16.2f} | {avgs_right["avg_queue_length"]:<10.2f} |')
