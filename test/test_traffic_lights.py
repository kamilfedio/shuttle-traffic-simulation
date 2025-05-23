from src.models.traffic_lights import (
    TrafficLight,
    TrafficLightState,
)


def _create_traffic_green_light():
    return TrafficLight.create(traffic_id=1, state=TrafficLightState.GREEN)


def _create_traffic_red_light():
    return TrafficLight.create(traffic_id=1, state=TrafficLightState.RED)


def test_traffic_light_creation_with_red_state():
    traffic_light = _create_traffic_red_light()
    assert traffic_light.traffic_id == 1
    assert traffic_light.state == TrafficLightState.RED


def test_traffic_light_creation_with_green_state():
    traffic_light = _create_traffic_green_light()
    assert traffic_light.traffic_id == 1
    assert traffic_light.state == TrafficLightState.GREEN

def test_traffic_light_change_state_from_green_to_red():
    traffic_light = _create_traffic_green_light()
    traffic_light.change_state()
    assert traffic_light.state == TrafficLightState.RED

def test_traffic_light_change_state_from_red_to_green():
    traffic_light = _create_traffic_red_light()
    traffic_light.change_state()
    assert traffic_light.state == TrafficLightState.GREEN


def test_traffic_light_change_one_cycle():
    traffic_light = _create_traffic_green_light()
    traffic_light.change_state()
    assert traffic_light.state == TrafficLightState.RED
    traffic_light.change_state()
    assert traffic_light.state == TrafficLightState.GREEN
    traffic_light.change_state()
    assert traffic_light.state == TrafficLightState.RED
