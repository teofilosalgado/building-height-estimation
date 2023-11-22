from dataclasses import dataclass
from datetime import date
from typing import List

from core.model.aoi import AOI
from core.model.tile import Tile


@dataclass
class Mosaic:
    aoi: AOI
    tiles: List[Tile]
    image_date: date
    image_path: str
