import os
import random
from datetime import date, datetime
from typing import List
from urllib.parse import urlsplit

from pyquadkey2 import quadkey
from settings import get_settings

from core.client.virtual_earth import VirtualEarthMetadataClient, VirtualEarthTileClient
from core.model import AOI, Mosaic, Tile


class MosaicRepository:
    def __init__(self) -> None:
        super().__init__()
        # Get properties from
        self.api_key = get_settings().api_key
        self.default_zoom_level = get_settings().default_zoom_level
        self.download_folder_path = get_settings().download_folder_path

        # Create metadata client
        self.virtual_earth_metadata_client = VirtualEarthMetadataClient(self.api_key)

        # Get properties from metadata
        complete_metadata = self.virtual_earth_metadata_client.get_complete()
        resources = next(iter(complete_metadata)).resources
        content = next(iter(resources))

        self.image_height = content.image_height
        self.image_width = content.image_width

        # Start tile client from metadata
        subdomain = random.choice(content.image_url_subdomains)
        tile_url_split = urlsplit(content.image_url)
        tile_url_template = f"{tile_url_split.scheme}://{tile_url_split.netloc}"

        generation = int("".join([n for n in tile_url_split.query if n.isdigit()]))
        tile_url = tile_url_template.format(**{"subdomain": subdomain})
        self.virtual_earth_tile_client = VirtualEarthTileClient(tile_url, generation)

    def _get_tiles_by_aoi(self, aoi: AOI) -> List[Tile]:
        # List to store results
        results: List[Tile] = []

        # List quadkeys to be downloaded
        top_left_quadkey = quadkey.from_geo(
            (aoi.envelope.max_x, aoi.envelope.max_y), self.default_zoom_level
        )
        bottom_right_quadkey = quadkey.from_geo(
            (aoi.envelope.min_x, aoi.envelope.min_y), self.default_zoom_level
        )
        quadkeys = quadkey.QuadKey.bbox([top_left_quadkey, bottom_right_quadkey])

        # Iterate over quadkeys to be downloaded
        for item in quadkeys:
            tile_coordinates = item.to_tile()
            tile_x = tile_coordinates[0][0]
            tile_y = tile_coordinates[0][1]
            tile_z = tile_coordinates[1]

            response = self.virtual_earth_tile_client.get(item.key)
            tile_file_name = f"{aoi.id}-{tile_x}-{tile_y}-{tile_z}.jpeg"
            tile_path = os.path.join(self.download_folder_path, tile_file_name)
            # Save downloaded tiles to disk
            with open(tile_path, "wb") as file:
                file.write(response.content)

            # Appende generated tile
            latitude, longitude = item.to_geo()
            results.append(Tile(tile_x, tile_y, tile_z, tile_path, longitude, latitude))
        return results

    def _get_image_date_by_aoi(self, aoi: AOI) -> date:
        centroid = f"{aoi.centroid[0]},{aoi.centroid[1]}"
        basic_metadata = self.virtual_earth_metadata_client.get_basic(
            self.default_zoom_level, centroid
        )
        resources = next(iter(basic_metadata)).resources
        content = next(iter(resources))
        result = datetime.strptime(content.vintage_end, "%d %b %Y GMT").date()
        return result

    def get_by_aoi(self, aoi: AOI) -> Mosaic:
        tiles = self._get_tiles_by_aoi(aoi)
        image_date = self._get_image_date_by_aoi(aoi)
        return Mosaic(
            self.image_height,
            self.image_width,
            aoi,
            tiles,
            image_date,
        )


def get_mosaic_repository():
    return MosaicRepository()
