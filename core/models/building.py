from typing import Tuple


class Building:
    def __init__(
        self, id: int, label: str, envelope: Tuple[int, int, int, int]
    ) -> None:
        self.id = id
        self.label = label
        self.envelope = envelope
