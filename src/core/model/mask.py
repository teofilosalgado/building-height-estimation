from dataclasses import dataclass

from core.model.mosaic import Mosaic


@dataclass
class Mask:
    mosaic: Mosaic
    file_path: str
