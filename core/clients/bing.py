import os
import random
from typing import Any, Dict, Generator, List

import requests
from clients import Base
from models import Tile
from pyquadkey2 import quadkey


class Bing(Base):
    imagery_metadata_aerial_url = (
        "https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial"
    )

    def __init__(
        self,
        default_zoom_level: int,
        download_folder_path: str,
        epsg: int,
        api_key: str,
    ) -> None:
        super().__init__(default_zoom_level, download_folder_path, epsg)

        # Initialize client-specific properties
        self.api_key = api_key

        # Get image download url from metadata
        response = requests.get(
            self.imagery_metadata_aerial_url,
            params={"key": self.api_key},
        )
        data = response.json()
        resource_sets: List[Dict[str, Any]] = data["resourceSets"]
        resource_set = next(iter(resource_sets))
        resources: List[Dict[str, Any]] = resource_set["resources"]
        resource = next(iter(resources))
        image_url_subdomains: List[str] = resource["imageUrlSubdomains"]

        self.subdomain: str = random.choice(image_url_subdomains)
        self.image_url_template: str = resource["imageUrl"]
        self.image_height: int = resource["imageHeight"]
        self.image_width: int = resource["imageWidth"]

    def download_tiles_from_envelope(
        self,
        min_x: float,
        max_x: float,
        min_y: float,
        max_y: float,
    ) -> Generator[Tile, None, None]:
        # List quadkeys to be downloaded
        top_left_quadkey = quadkey.from_geo((max_x, max_y), self.default_zoom_level)
        bottom_right_quadkey = quadkey.from_geo((min_x, min_y), self.default_zoom_level)
        quadkeys = quadkey.QuadKey.bbox([top_left_quadkey, bottom_right_quadkey])

        # Iterate over quadkeys to be downloaded
        for item in quadkeys:
            tile_coordinates = item.to_tile()
            tile_x = tile_coordinates[0][0]
            tile_y = tile_coordinates[0][1]
            tile_z = tile_coordinates[1]
            download_url = self.image_url_template.format(
                **{"subdomain": self.subdomain, "quadkey": item.key}
            )
            response = requests.get(download_url, allow_redirects=True)
            tile_path = os.path.join(
                self.download_folder_path, f"{tile_x}-{tile_y}-{tile_z}.jpeg"
            )
            # Save downloaded tiles to disk
            with open(tile_path, "wb") as file:
                file.write(response.content)
            # Appende generated tile
            yield Tile(tile_x, tile_y, tile_z, tile_path)
