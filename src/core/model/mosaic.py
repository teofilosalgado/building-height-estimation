import os
from datetime import date
from typing import Dict, List, Tuple

import rasterio
from PIL import Image
from rasterio.control import GroundControlPoint
from rasterio.transform import from_gcps

from core.model.aoi import AOI
from core.model.tile import Tile


class Mosaic:
    def __init__(
        self,
        download_folder_path: str,
        tile_height: int,
        tile_width: int,
        aoi: AOI,
        tiles: List[Tile],
        image_date: date,
    ) -> None:
        self.aoi = aoi
        self.tiles = tiles
        self.image_date = image_date

        # Sort tiles from top left to bottom right
        sorted_tiles = sorted(self.tiles, key=lambda item: [item.y, item.x])

        # Calculate mosaic dimensions
        top_left_quadkey = next(iter(sorted_tiles))
        bottom_right_quadkey = next(reversed(sorted_tiles))
        total_width = tile_width * (bottom_right_quadkey.x - top_left_quadkey.x + 1)
        total_height = tile_height * (bottom_right_quadkey.y - top_left_quadkey.y + 1)

        # Lookup table to speed up stitching
        sorted_lookup: Dict[Tuple[int, int], Tile] = {
            (tile.x, tile.y): tile for tile in sorted_tiles
        }

        # Stitch tiles into a mosaic, creating ground control points to
        # georeference the final image
        merged_image = Image.new("RGB", (total_width, total_height))
        ground_control_points: List[GroundControlPoint] = []
        for x in range(top_left_quadkey.x, bottom_right_quadkey.x + 1):
            for y in range(top_left_quadkey.y, bottom_right_quadkey.y + 1):
                tile = sorted_lookup[(x, y)]
                tile_image = Image.open(tile.file_path)

                x_offset = (x - top_left_quadkey.x) * tile_width
                y_offset = (y - top_left_quadkey.y) * tile_height
                ground_control_point = GroundControlPoint(
                    y_offset, x_offset, tile.longitude, tile.latitude
                )
                ground_control_points.append(ground_control_point)

                merged_image.paste(tile_image, (x_offset, y_offset))
                tile_image.close()

        # Export mosaic as tiff
        merged_image_path = os.path.join(download_folder_path, f"{aoi.id}-merged.tiff")
        merged_image.save(merged_image_path, quality=100)
        merged_image.close()

        # Georeference mosaic
        transform = from_gcps(ground_control_points)

        with rasterio.open(merged_image_path, "r+") as ds:
            ds.crs = "epsg:4326"
            ds.transform = transform
