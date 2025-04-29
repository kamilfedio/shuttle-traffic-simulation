from src.models.lights_system import LightsSystem
from src.models.traffic_lights import TrafficLightState, TrafficLight


def _create_traffic_lights():
    return LightsSystem.create(traffic_state=TrafficLightState.GREEN, num_drivers=5)


def test_create_lights_system():
    lights_system: LightsSystem = _create_traffic_lights()
    assert lights_system is not None
    assert isinstance(lights_system.traffic_lights, TrafficLight)
    assert lights_system.num_drivers == 5
    assert lights_system.lights_timestamps is None
    assert lights_system.drivers_timestamps is None


def test_lights_timestamps():
    lights_system: LightsSystem = _create_traffic_lights()
    assert lights_system.lights_timestamps is None
    lights_system.lights_timestamps = [(TrafficLightState.RED, 1), (TrafficLightState.GREEN, 2)]
    assert lights_system.lights_timestamps == [(TrafficLightState.RED, 1), (TrafficLightState.GREEN, 2)]
    lights_system.lights_timestamps = [(TrafficLightState.RED, 1)]
    assert lights_system.lights_timestamps == [(TrafficLightState.RED, 1)]

def test_drivers_timestamps():
    lights_system: LightsSystem = _create_traffic_lights()
    assert lights_system.drivers_timestamps is None
    lights_system.drivers_timestamps = [1, 2, 3, 4, 5]
    assert lights_system.drivers_timestamps == [1, 2, 3, 4, 5]
