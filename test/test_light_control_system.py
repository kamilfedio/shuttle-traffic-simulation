from src.models.light_control_system import ControlSystem
'''
- przy tworzeniu ładuje basetiome zielonego (w nowej wersji będzie to tylko do 1 iteracji - gdy nie ma alpha.
  Najlepiej gdyby w pętli: generowanie tupli czasów, queue.run(), pobieranie danych kolejkowych do next loopa
- przyjmuje queue1 i queue2, q1 będzie teraz zielona
- wypluwa tuple(zielone, zielone + 5)
'''


def _create_light_control_system(basetime: float | int, alpha: int | float = None):
    return ControlSystem.create_control_system(basetime, alpha)


def test_create_light_control_system():
    control_system: ControlSystem = _create_light_control_system(15)
    assert control_system is not None
    isinstance(control_system, ControlSystem)
    assert control_system.basetime == 15
    assert not control_system.alpha


def test_calculate_time():
    control_system: ControlSystem = _create_light_control_system(15)
    assert control_system.calculate_time(0, 0) == (15, 20)
    assert control_system.calculate_time(10, 10) == (15, 20)
    assert control_system.calculate_time(0, 2) == (15, 20)
    assert control_system.calculate_time(-4, 0) == (15, 20)
    assert control_system.calculate_time(1000, 0) == (15, 20)

def test_calculate_time_alpha():
    control_system: ControlSystem = _create_light_control_system(15, 2)
    assert control_system.calculate_time(1, 0) == (30, 35)
    assert control_system.calculate_time(1, 0)[::-1] == (35, 30)
    assert control_system.calculate_time(1, 1) == (15, 20)
    assert control_system.calculate_time(0, 1) == (7.5, 12.5)
