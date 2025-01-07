from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState
from src.models.driver import Driver




def _create_queue() -> Queue:
    lightssystem = LightsSystem.create(traffic_state=TrafficLightState.GREEN, num_drivers=5)
    lightssystem.generate_lights_timestamps()
    lightssystem.generate_drivers()
    return Queue.create_queue(lightssystem.drivers, lightssystem.lights_timestamps)


def test_create_queue():
    queue: Queue = _create_queue()
    isinstance(queue.light_timestamps, list)

    assert queue.current_time == 0
    for driver in queue.drivers:
        isinstance(driver, Driver)
    for light in queue.light_timestamps:
        state, stamp = light
        isinstance(state, TrafficLightState)
        isinstance(stamp, float)
        assert stamp >= 0


def test_update_lights():
    queue: Queue = _create_queue()
    queue.update_lights()