from typing import List, Any
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


def print_simulation_summary(blackbox: dict[str, Any]) -> None:
    print(f'\n\n{"S T A T S":^158}')
    print("-" * 158)
    print(f'| DIRECTION | FIRST COLOR | DRIVERS SERVED | NO-WAIT DRIVERS | AVG WAIT TIME | AVG GREEN WAIT TIME | '
          f'AVG DRIVERS BEHIND | AVG QUEUE LENGTH | AVG CYCLE WAITS |')
    print('-' * 158)
    for key, blackbox in blackbox.items():
        print(
            f"| {blackbox['direction']:<9} | {blackbox['first_color']:<11} | {blackbox['avgs']['drivers_served']:<14} | {blackbox['avgs']['no_stop_drivers']:<15} | {blackbox['avgs']['avg_waiting_times']:<13.2f} | "
            f"{blackbox['avgs']['avg_green_waiting_times']:<19.2f} | {blackbox['avgs']['avg_queue_length']:<18.2f} | "
            f"{blackbox['avg_queue_length']:<16.2f} | {blackbox['avg_cycle_wait']:<15.2f} |")
        print('-' * 158)


def print_cycle_summary(data: tuple, direction: str, is_left_green: bool = True) -> None:
    if is_left_green:
        print(f'\n{direction}')
        print(data[0], data[1])
        print(f'GREEN: {data[2]}')
        print(f'RED: {data[3]}')
    else:
        if is_left_green:
            print(f'\n{direction}')
            print(data[0], data[1])
            print(f'RED: {data[2]}')
            print(f'GREEN: {data[3]}')