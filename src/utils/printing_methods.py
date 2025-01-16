from typing import List
from src.models.queue import Queue


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
