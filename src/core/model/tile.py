from dataclasses import dataclass


@dataclass
class Tile:
    x: int
    y: int
    z: int
    file_path: str
