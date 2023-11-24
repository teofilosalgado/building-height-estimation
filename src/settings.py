from functools import lru_cache
from typing import ClassVar

from osgeo import osr
from pydantic_settings import BaseSettings, SettingsConfigDict
from rasterio.crs import CRS


class Settings(BaseSettings):
    api_key: str
    default_zoom_level: int
    download_folder_path: str

    spatial_reference: ClassVar[osr.SpatialReference] = osr.SpatialReference(
        wkt=CRS.from_epsg(4326).wkt
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        arbitrary_types_allowed=True,
    )


@lru_cache
def get_settings():
    return Settings()  # type: ignore
