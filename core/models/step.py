from dataclasses import dataclass
from typing import List, Tuple

from models import State


@dataclass
class GetEnvelopeFromFeatureState:
    id: int
    label: str
    envelope: Tuple[int, int, int, int]


class InitialStep(State):
    def next(self, next_state: List[GetEnvelopeFromFeatureState]) -> None:
        self.context.transition_to(GetEnvelopeFromFeature(next_state))


class GetEnvelopeFromFeature(State):
    def __init__(self, state: List[GetEnvelopeFromFeatureState]) -> None:
        self.state = state

    def next(self) -> None:
        pass
