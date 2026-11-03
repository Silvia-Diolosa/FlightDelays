from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Tratta:
    aeroportoP: Airport
    aeroportoA: Airport
    peso: int