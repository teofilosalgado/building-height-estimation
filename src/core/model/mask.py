from dataclasses import dataclass

from osgeo import ogr

from core.model.mosaic import Mosaic


@dataclass
class Mask:
    mosaic: Mosaic
    file_path: str
    shadow_area: ogr.Geometry
