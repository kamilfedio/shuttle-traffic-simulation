from src.models.simulation import Simulation
from tqdm import tqdm
import pandas as pd


class Evaluation:
    def __init__(self, repetitions: int) -> None:
        self.repetitions: int = repetitions
        self.data_normal = []
        self.data_control_system = []

    @classmethod
    def create(cls, repetitions: int) -> "Evaluation":
        return cls(repetitions)

    def evaluate(self, case: tuple[str, str]):
        left, right = case
        for _ in tqdm(range(self.repetitions)):
            simulation = Simulation.create(left_intensity=left, right_intensity=right, use_control_system=False)
            simulation.simulate()
            self.data_normal.append(simulation.get_data)

            simulation = Simulation.create(left_intensity=left, right_intensity=right, use_control_system=True)
            simulation.simulate()
            self.data_control_system.append(simulation.get_data)

    @property
    def get_results_normal(self):
        return self.data_normal

    @property
    def get_results_control_system(self):
        return self.data_control_system


cases = [('low', 'low'), ('low', 'mid')]# ('low', 'high'), ('mid', 'mid'), ('mid', 'high'), ('high', 'high')]
results_normal = []
results_control_system = []

for left, right in cases:
    evaluation = Evaluation.create(3)
    evaluation.evaluate((left, right))
    results_normal.append(evaluation.get_results_normal)
    results_control_system.append(evaluation.get_results_control_system)

print(results_normal)
print()
df_norm = pd.DataFrame.from_dict(results_normal[0])
print(df_norm)
