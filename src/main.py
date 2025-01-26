import numpy as np
from src.models.simulation import Simulation

np.random.seed(42)


simulation = Simulation.create(is_debugging=True, left_intensity='mid')
simulation.simulate()
