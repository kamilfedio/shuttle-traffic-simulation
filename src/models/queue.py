from typing import List, Any
from src.models.driver import Driver
from src.models.traffic_lights import TrafficLightState
from src.models.lights_system import LightsSystem

'''
Co to ma robic?
-x przechowuje obecnych Driverów
-x przyjmuje timestamp i updatuje kolejke jedną metodą (lista driverow)
-x usuwa driverów, jeśli ich departure_time jest mniejszy niz red_light_time to sobie jadom, dodawani do happy_drivers
-x zbiera dane o kolejce
-x metoda run która obsługuję tę stronę kolejki (timestamp czerwonego)
'''


class Queue:
    def __init__(
            self,
            light_system: LightsSystem,
            light_state: bool,
            green_timestamp: float | None = None,
            red_timestamp: float | None = None
    ):
        self.cars: List[Driver] = []
        self.current_time: float = 0
        self.light_system: LightsSystem = light_system
        self.red_timestamp: float | None = red_timestamp
        self.green_timestamp: float | None = green_timestamp
        self.light_state: bool = light_state
        self.happy_drivers: List[Driver] = []
        self._blackbox: List[dict] = list()
        self.last_avg_waiting_time: List[float] = list()
        self.counter: int = -1

    def enqueue(self, car):
        self.cars.append(car)

    def dequeue(self, penalty) -> bool:
        if self.is_empty():
            return False

        driver = self.cars[0]
        moved = driver.arrived_timestamp if driver.arrived_timestamp > self.current_time else self.current_time + penalty + driver.reaction_time

        if moved <= self.red_timestamp:
            driver = self.cars.pop(0)
            driver.black_box = {"drivers_in_queue": self.length(moved),
                                "waiting_time": round(float(moved - driver.arrived_timestamp), 4),
                                "moved_time": round(float(moved), 4)}
            self.current_time = moved
            self.happy_drivers.append(driver)
            self.last_avg_waiting_time.append(driver.black_box['waiting_time'])
            return True

        return False

    def is_empty(self) -> bool:
        return len(self.cars) == 0

    def length(self, moved: float) -> int:
        return len([car for car in self.cars if car.arrived_timestamp <= moved])

    @classmethod
    def create_queue(cls, lights_system: LightsSystem) -> "Queue":
        lights_system.generate_lights_timestamps()
        lights_system.generate_drivers()

        state, stamp = lights_system.lights_timestamps.pop(0)
        if state == TrafficLightState.GREEN:
            return cls(
                lights_system,
                True,
                green_timestamp=stamp
            )

        return cls(
            lights_system,
            False,
            red_timestamp=stamp
        )

    def update(self, timestamp):
        if self.light_system.drivers and self.light_system.drivers[0].arrived_timestamp <= timestamp + 5:
            self.enqueue(self.light_system.drivers.pop(0))
            self.update(timestamp)

    def update_lights(self):
        self.light_system.swap_lights()
        state, stamp = self.light_system.lights_timestamps.pop(0)
        if state == TrafficLightState.GREEN:
            self.light_state = True
            self.green_timestamp = stamp
        else:
            self.light_state = False
            self.red_timestamp = stamp

    @property
    def black_box(self) -> List[dict]:
        return self._blackbox

    @black_box.setter
    def black_box(self, value: dict) -> None:
        self._blackbox.append(value)

    def run(self, light_times: tuple[float, ...] | None = None) -> None:
        drove: int = 0
        self.counter += 1
        if light_times:
            self.light_system.generate_lights_timestamps(light_times)
            self.light_system.lights_timestamps = self.light_system.lights_timestamps[self.counter:]

        time_penalty = 0
        if self.light_state:
            self.update_lights()
            self.update(self.red_timestamp)
            if not self.is_empty():
                self.current_time = self.green_timestamp
                skibidi = self.dequeue(time_penalty)
                time_penalty += 1
                while skibidi:
                    drove += 1
                    skibidi = self.dequeue(time_penalty)
                    time_penalty += 1
        else:
            self.update_lights()
            self.update(self.green_timestamp)

        data: dict[str, Any] = dict()
        if not self.light_state:
            data["drove"] = drove
            data["avg_waiting_time"] = round(sum(self.last_avg_waiting_time) / len(
                self.last_avg_waiting_time), 4) if drove > 0 else 0
            data["queue"] = self.length(self.red_timestamp + 5)
        else:
            data["queue"] = self.length(self.green_timestamp)

        self.last_avg_waiting_time = list()

        if len(self.black_box) == 0 or len(self.black_box[-1].keys()) == 3:
            self.black_box.append(data)
        else:
            self.black_box[-1].update(data)

    def scan_queue(self) -> int:
        return self._blackbox[-1]['queue']
