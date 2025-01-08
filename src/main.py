from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState

left_light_system: LightsSystem = LightsSystem.create(TrafficLightState.GREEN, 100)
print(left_light_system.traffic_lights.state)
left_light_system.generate_lights_timestamps()
print(left_light_system.lights_timestamps)

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

print(left_queue.light_timestamps)
print(left_queue.light_state)
left_queue.run()
left_queue.run()
left_queue.run()

for i in left_queue.happy_drivers:
    print(i.black_box, i.name, i.driver_id)
    print()