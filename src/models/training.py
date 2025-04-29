from src.models.simulation import Simulation
from typing import List
from tqdm import tqdm
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt


class Training:
    def __init__(self, precision: int, floor: int | float, ceil: int | float) -> None:
        self.precision: int = precision
        self.floor: int | float = floor
        self.ceil: int | float = ceil
        self.alpha_results: dict = {}
        self.new_range: List[int, float] = []
        self.intensity_cases: List[tuple] = [('low', 'low'), ('low', 'mid'), ('low', 'high'), ('mid', 'mid'),
                                             ('mid', 'high'), ('high', 'high')]

    @classmethod
    def create(cls, precision: int, floor: int | float, ceil: int | float) -> 'Training':
        return cls(precision, floor, ceil)

    def eval_range(self):
        candidates: npt.NDArray[float] = np.linspace(self.floor, self.ceil, 15, endpoint=True)
        results: dict[int | float, int | float] = {}

        for alpha in tqdm(candidates):
            results_for_alpha: List[float] = []
            for left, right in self.intensity_cases:
                temp_result = 0
                for _ in range(10):
                    simulation = Simulation.create(is_training=True, left_intensity=left, right_intensity=right,
                                                   alpha=alpha)
                    temp_result += simulation.simulate()
                results_for_alpha.append(temp_result / 10)
            results[alpha] = np.average(results_for_alpha)

        self.alpha_results.update(results)
        return results

    def _set_new_range(self, results: dict[float, int]):
        self.new_range = [alpha for alpha in sorted(results, key=results.get)][0:7]
        diff = abs(self.new_range[6] - self.new_range[0])
        _floor = self.new_range[0] - diff
        self.floor = _floor if _floor >= 1 else 1
        self.ceil = self.new_range[0] + diff

    def train(self):
        for iteration in range(self.precision):
            iteration_results = self.eval_range()
            self._set_new_range(iteration_results)
            print(f'\nIteration {iteration+1} best alpha values: {self.new_range}')
        print(f'\nBest alpha: {self.new_range[0]}, avg time: {self.alpha_results[self.new_range[0]]}')

    def make_chart(self):
        alphas = []
        avgs = []
        for key, val in sorted(self.alpha_results.items(), key=lambda x: x[0]):
            if val < 35:
                alphas.append(key)
                avgs.append(val)

        plt.yscale("log")
        plt.plot(alphas, avgs)
        plt.xlabel('Alpha')
        plt.ylabel('AVG wait time (LOG scale)')
        plt.title('Alpha values and their corresponding waiting times')
        plt.show()


training = Training.create(6, 1, 1.2)
training.train()
training.make_chart()
