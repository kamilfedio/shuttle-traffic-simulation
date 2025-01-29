from typing import Any

import numpy as np

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


cases = [('low', 'low'), ('low', 'mid')]# ('low', 'mid') ('low', 'high'), ('mid', 'mid'), ('mid', 'high'), ('high', 'high')]
results_normal = []
results_control_system = []

for left, right in cases:
    evaluation = Evaluation.create(3)
    evaluation.evaluate((left, right))
    results_normal.append(evaluation.get_results_normal)
    results_control_system.append(evaluation.get_results_control_system)


def get_res(results):
    data_values: list[dict[str, Any]] = []
    for case in results:
        cases_values = {}
        for tries in case:
            for queue, data in tries.items():
                for key, value in data.items():
                    if key == 'avgs':
                        for k, avg in value.items():
                            keyname: str = f'{queue}_{key}_{k}'

                            if not cases_values.get(keyname):
                                cases_values[keyname] = []

                            cases_values[keyname].append(avg)

                    else:
                        keyname: str = f'{queue}_{key}'

                        if not cases_values.get(keyname):
                            cases_values[keyname] = []

                        cases_values[keyname].append(value)

        data_values.append(cases_values)

    for dicti in data_values:
        for k, v in dicti.items():
            if 'queue_avgs_no_stop_drivers' in k:
                tmp = [float(i[:-1]) for i in v]
                dicti[k] = np.mean(tmp)
            elif 'avgs' in k:
                dicti[k] = np.mean(v)
            else:
                dicti[k] = v[0]

    return data_values

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

control_system_res = get_res(results_control_system)
normal_res = get_res(results_normal)

df_norm = pd.DataFrame.from_records(normal_res)
df_control = pd.DataFrame.from_records(control_system_res)
print(df_norm)
print(df_control)
