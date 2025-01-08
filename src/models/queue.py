from typing import List
from src.models.driver import Driver
from src.models.traffic_lights import TrafficLightState

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
            drivers: List[Driver],
            light_timestamps: List[tuple],
            light_state: bool,
            green_timestamp: float | None = None,
            red_timestamp: float | None = None
    ):
        self.cars: List[Driver] = []
        self.current_time: float = 0
        self.drivers: List[Driver] = drivers
        self.red_timestamp: float | None = red_timestamp
        self.green_timestamp: float | None = green_timestamp
        self.light_timestamps: List[tuple] = light_timestamps[1:]
        self.light_state: bool = light_state
        self.happy_drivers: List[Driver] = []

    def enqueue(self, car):
        self.cars.append(car)

    def dequeue(self, penalty) -> bool:
        if self.is_empty():
            return False
        driver = self.cars[0]
        if driver.arrived_timestamp > self.current_time:
            moved = driver.arrived_timestamp
            if moved <= self.red_timestamp:
                driver = self.cars.pop(0)
                driver.black_box = {"Drivers in queue": self.length(moved),
                                    "Waiting time": round(float(moved - driver.arrived_timestamp), 4),
                                    "Arrived time": round(float(driver.arrived_timestamp), 4),
                                    "Moved time": round(float(moved), 4)}
                self.current_time = moved
                self.happy_drivers.append(driver)
                return True
        else:
            moved = self.current_time + penalty + driver.reaction_time
            if moved <= self.red_timestamp:
                driver = self.cars.pop(0)
                driver.black_box = {"Drivers in queue": self.length(moved),
                                    "Waiting time": round(float(moved - driver.arrived_timestamp), 4),
                                    "Arrived time": round(float(driver.arrived_timestamp), 4),
                                    "Moved time": round(float(moved), 4)}
                self.current_time = moved
                self.happy_drivers.append(driver)
                return True
        return False

    def is_empty(self) -> bool:
        return len(self.cars) == 0

    def length(self, moved: float) -> int:
        return len([car for car in self.cars if car.arrived_timestamp <= moved])

    @classmethod
    def create_queue(cls, drivers: List[Driver], light_timestamps: List[tuple]) -> "Queue":
        state, stamp = light_timestamps[0]
        if state == TrafficLightState.GREEN:
            return cls(
                drivers,
                light_timestamps,
                True,
                green_timestamp=stamp
            )

        return cls(
            drivers,
            light_timestamps,
            False,
            red_timestamp=stamp
        )

    def update(self, timestamp):
        if self.drivers and self.drivers[0].arrived_timestamp <= timestamp:
            self.enqueue(self.drivers.pop(0))
            self.update(timestamp)

    def update_lights(self):
        state, stamp = self.light_timestamps.pop(0)
        if state == TrafficLightState.GREEN:
            self.light_state = True
            self.green_timestamp = stamp
        else:
            self.light_state = False
            self.red_timestamp = stamp

    def run(self):
        time_penalty = 0
        if self.light_state:
            self.update_lights()
            self.update(self.red_timestamp)
            if not self.is_empty():
                self.current_time = self.green_timestamp
                skibidi = self.dequeue(time_penalty)
                time_penalty += 1
                while skibidi:
                    skibidi = self.dequeue(time_penalty)
                    time_penalty += 1
        else:
            self.update_lights()
            self.update(self.green_timestamp)
