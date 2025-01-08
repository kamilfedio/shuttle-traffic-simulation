from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState
from typing import List
from numpy import random

left_light_system: LightsSystem = LightsSystem.create(TrafficLightState.GREEN, 100)
left_queue: Queue = Queue.create_queue(
    left_light_system
)

right_light_system: LightsSystem = LightsSystem.create(TrafficLightState.RED, 100)
right_queue: Queue = Queue.create_queue(
    right_light_system
)


def print_que_state(queue: Queue, cosh: List):
    print()
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

    print()


def print_red_queue(queue: Queue):
    print()
    print(f'| {"STATUS":<7} | {"ID":<3} | {"Driver Name":<13} | {"Arrived Time [s]":<17} |')
    print('-' * 53)
    if not queue.cars:
        print('| WAITING |')
    for driver in queue.cars:
        print(f'| WAITING'
              f' | {str(driver.driver_id).zfill(3)}'
              f' | {driver.name:<13}'
              f' | {driver.black_box.get("arrived_time", ""):<17} |')

    print()


cosh1 = []
cosh2 = []


def run_cycle(queue1: Queue, queue2: Queue):
    if queue1.light_state:
        if random.randint(0, 3) == 1:
            queue2.run(light_times=(20, 30))
        else:
            queue2.run(light_times=(15, 20))
        print_red_queue(queue2)
        queue1.run()
        print_que_state(queue1, cosh1)
    else:
        queue1.run()

        queue2.run()
        print_que_state(queue2, cosh2)
        print_red_queue(queue1)


for cycle in range(20):
    print('-' * 112)
    cycle_title = f'CYCLE {cycle}'
    print(f'\n{cycle_title:^112}\n')
    run_cycle(left_queue, right_queue)

print(left_queue.black_box)
print(right_queue.black_box)