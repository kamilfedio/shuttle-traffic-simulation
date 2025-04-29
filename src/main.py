import numpy as np
from src.models.simulation import Simulation



simulation = Simulation.create(is_debugging=True, left_intensity='mid', right_intensity='mid', use_control_system=False)
simulation.simulate()

print(simulation.get_avg_wait_time())