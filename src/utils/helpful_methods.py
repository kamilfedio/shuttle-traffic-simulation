import numpy as np

from src.models.queue import Queue


def _avg_waiting_times(queue: Queue):
    waiting_times = [happy_driver.black_box.get('waiting_time', 0) for happy_driver in queue.happy_drivers]
    no_stop = sum([1 for happy_driver in queue.happy_drivers if happy_driver.black_box.get('waiting_time', 0) == 0])
    green_waiting_times = [happy_driver.black_box.get('green_wait_time', 0) for happy_driver in queue.happy_drivers]
    queue_length = [happy_driver.black_box.get('drivers_in_queue', 0) for happy_driver in queue.happy_drivers]
    served = len(queue.happy_drivers)
    return {'avg_waiting_times': np.mean(waiting_times),
            'avg_green_waiting_times': np.mean(green_waiting_times),
            'avg_queue_length': np.mean(queue_length),
            'drivers_served': served,
            'no_stop_drivers': str(round(100 * no_stop / served, 2))+"%"}