from abc import abstractmethod
from typing import Generator

from models import Tile
from osgeo import osr


class Base:
    def __init__(
        self,
        default_zoom_level: int,
        download_folder_path: str,
        epsg: int,
    ) -> None:
        self.default_zoom_level = default_zoom_level
        self.download_folder_path = download_folder_path

        # Default spatial reference used by client
        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromEPSG(epsg)
        self.spatial_reference = spatial_reference

    @abstractmethod
    def download_tiles_from_envelope(
        self,
        min_x: float,
        max_x: float,
        min_y: float,
        max_y: float,
    ) -> Generator[Tile, None, None]:
        pass
