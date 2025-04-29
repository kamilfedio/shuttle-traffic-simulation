from typing import Any

import numpy as np

from src.models.queue import Queue
from src.models.traffic_lights import TrafficLightState


def avg_waiting_times(queue: Queue):
    waiting_times = [happy_driver.black_box.get('waiting_time', 0) for happy_driver in queue.happy_drivers]
    no_stop = sum([1 for happy_driver in queue.happy_drivers if happy_driver.black_box.get('waiting_time', 0) == 0])
    green_waiting_times = [happy_driver.black_box.get('green_wait_time', 0) for happy_driver in queue.happy_drivers]
    queue_length = [happy_driver.black_box.get('drivers_in_queue', 0) for happy_driver in queue.happy_drivers]
    served = len(queue.happy_drivers)
    return {'avg_waiting_times': np.mean(waiting_times),
            'avg_green_waiting_times': np.mean(green_waiting_times),
            'avg_queue_length': np.mean(queue_length),
            'drivers_served': served,
            'no_stop_drivers': str(round(100 * no_stop / served, 2) if served > 0 else 0) + "%"}


def create_blackbox(queue: Queue, direction: str) -> dict[str, Any]:
    avgs_times = avg_waiting_times(queue)
    avg_queue_length = np.mean([cell["queue"] for cell in queue.black_box])
    avg_cycle_wait = np.mean([cell["cycle_wait"] for cell in queue.black_box if len(cell.keys()) > 1])

    return {
        'avgs': avgs_times,
        'avg_queue_length': avg_queue_length,
        'avg_cycle_wait': avg_cycle_wait,
        'direction': direction
    }


def get_eval_avg(blackbox: dict[str, Any]) -> float:
    _temp_val: float = 0
    for key, blackbox in blackbox.items():
        _temp_val += blackbox['avgs']['avg_waiting_times']
    return _temp_val / 2
