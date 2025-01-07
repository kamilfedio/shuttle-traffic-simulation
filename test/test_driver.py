from src.models.driver import Driver

def _create_driver() -> Driver:
    return Driver.generate_driver(0)

def test_driver_create():
    driver: Driver = _create_driver()
    assert driver.driver_id == 0
    assert isinstance(driver.arrived_time, float)
    assert driver.arrived_time > 0
    assert isinstance(driver.black_box, dict)
    assert driver._arrived_timestamp is None
    assert isinstance(driver.reaction_time, float)
    assert isinstance(driver.lays, bool)
    assert isinstance(driver.red_running_time, float)

def test_driver_set_arrived_timestamp():
    driver: Driver = _create_driver()
    driver.arrived_timestamp = 100
    assert driver.arrived_timestamp == 100

def test_driver_set_blackbox():
    driver: Driver = _create_driver()
    driver.black_box = {"test": 1}
    assert driver.black_box == {"test": 1}

def test_driver_set_multi_blackbox():
    driver: Driver = _create_driver()
    driver.black_box = {"test": 1, "test2": 2}
    assert driver.black_box == {"test": 1, "test2": 2}
