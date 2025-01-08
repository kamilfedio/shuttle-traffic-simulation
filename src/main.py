from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState
from typing import List

left_light_system: LightsSystem = LightsSystem.create(TrafficLightState.GREEN, 100)
left_light_system.generate_lights_timestamps()

left_light_system.generate_drivers()
left_queue: Queue = Queue.create_queue(
    left_light_system.drivers, left_light_system.lights_timestamps
)

right_light_system: LightsSystem = LightsSystem.create(TrafficLightState.RED, 100)
right_light_system.generate_lights_timestamps()
right_light_system.generate_drivers()
right_queue: Queue = Queue.create_queue(
    right_light_system.drivers, right_light_system.lights_timestamps
)


def print_que_state(queue: Queue, cosh: List):
    print()
    for driver in queue.happy_drivers:
        if driver not in cosh:
            print(f'{driver.black_box, str(driver.name), driver.driver_id}')
            cosh.append(driver)
    print()


def print_red_queue(queue: Queue):
    print()
    for driver in queue.cars:
        print(f'WAITING: {driver.black_box, str(driver.name), driver.driver_id}')


cosh1 = []
cosh2 = []
space = ' '


def run_cycle(queue1: Queue, queue2: Queue):
    if queue1.light_state:
        print('Green' if queue2.light_state else 'Red')
        queue2.run()
        print_red_queue(queue2)
        print('  -  '*30)
        print('Green' if queue1.light_state else 'Red')
        queue1.run()
        print_que_state(queue1, cosh1)
    else:
        l1_temp = queue1.light_state
        queue1.run()

        print('Green' if queue2.light_state else 'Red')
        queue2.run()
        print_que_state(queue2, cosh2)
        print('  -  '*30)
        print('Green' if l1_temp else 'Red')
        print_red_queue(queue1)


for cycle in range(20):
    print('-' * 150)
    print(f'\n{space*75}CYCLE {cycle}\n')
    run_cycle(left_queue, right_queue)
