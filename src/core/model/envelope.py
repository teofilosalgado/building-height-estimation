from dataclasses import dataclass


@dataclass
class Envelope:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
