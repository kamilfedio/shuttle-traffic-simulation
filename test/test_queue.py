from src.models.queue import Queue
from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState
from src.models.driver import Driver


def _create_queue() -> Queue:
    light_system: LightsSystem = LightsSystem.create(TrafficLightState.GREEN, 100)
    return Queue.create_queue(light_system)


def test_create_queue():
    queue: Queue = _create_queue()
    isinstance(queue.light_system, LightsSystem)
    isinstance(queue.light_system.lights_timestamps, list)
    assert queue.light_state
    assert queue.red_timestamp is None
    assert queue.current_time == 0
    for driver in queue.light_system.drivers:
        isinstance(driver, Driver)
    for light in queue.light_system.lights_timestamps:
        state, stamp = light
        isinstance(state, TrafficLightState)
        isinstance(stamp, float)
        assert stamp >= 0
    assert queue.is_empty()


def test_update_lights():
    queue: Queue = _create_queue()
    queue.update_lights(15, 20)
    assert queue.red_timestamp is not None
    assert queue.red_timestamp != queue.green_timestamp


def test_run():
    queue: Queue = _create_queue()
    queue.run((15, 20))
    if queue.light_system.drivers[0].arrived_timestamp < 20:
        assert queue.happy_drivers
    assert not queue.light_state
    if 25 > queue.light_system.drivers[0].arrived_timestamp > 20:
        assert not queue.is_empty()
        assert queue._blackbox[-1]['queue'] > 0
    if queue.is_empty():
        assert queue._blackbox[-1]['queue'] == 0


def test_update():
    queue: Queue = _create_queue()
    if queue.light_system.drivers[0].arrived_timestamp <= 50:
        queue.update(50)
        assert queue.cars
        for car in queue.cars:
            isinstance(car, Driver)
            assert car.arrived_timestamp <= 50
