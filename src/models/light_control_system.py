'''
Co to ma robic?
- przyjmuje bieżący stan świateł (które teraz będzie zielone i ile osób w kolejce) queue1 jest zielone
- oblicza różnicę długości kolejek i wstawia ją jako x do funkcji a * x = y, gdzie y to mnożnik bazowego czasu zielonego światła
  (jego trzeba zoptymalizować najpierw, żebyśmy mieli optymalny baseline dla x = 0)
- trzeba jakoś znaleźć optymalną wartość a, może brute force wypróbować różne wartości np. od 0 do 10 i zobaczyć jakie dają wyniki
  na wykresie
'''


class ControlSystem:
    def __init__(
            self,
            basetime: float | int,
            alpha: float | None
    ):
        self.basetime: float | int = basetime
        self.alpha: float | None = alpha

    @classmethod
    def create_control_system(cls, basetime: float | int, alpha: float | None = None) -> "ControlSystem":
        return cls(basetime, alpha)

    def calculate_time(self, queue1: int, queue2: int) -> tuple[float, ...]:
        difference: int = queue1 - queue2
        print(type(self.alpha))
        if self.alpha:
            green_time: float = (self.alpha ** difference) * self.basetime
            print(self.alpha, difference, self.basetime)
            return tuple([green_time, green_time + 5])
        return tuple([self.basetime, self.basetime + 5])
