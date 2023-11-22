from abc import abstractmethod
from datetime import date
from typing import List

from osgeo import osr

from core.model import Tile


class Base:
    def __init__(
        self,
        epsg: int,
        default_zoom_level: int,
        download_folder_path: str,
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
    ) -> List[Tile]:
        pass

    @abstractmethod
    def get_imagery_date_from_centroid(self, x: float, y: float) -> date:
        pass

    @property
    @abstractmethod
    def image_height(self) -> int:
        pass

    @property
    @abstractmethod
    def image_width(self) -> int:
        pass
