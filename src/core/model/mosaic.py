import os
from datetime import date
from typing import Dict, List, Tuple

from osgeo import gdal, osr
from PIL import Image

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

        # Calculate final image dimensions
        top_left_quadkey = next(iter(sorted_tiles))
        bottom_right_quadkey = next(reversed(sorted_tiles))
        total_width = tile_width * (bottom_right_quadkey.x - top_left_quadkey.x + 1)
        total_height = tile_height * (bottom_right_quadkey.y - top_left_quadkey.y + 1)

        # Lookup table to speed up final image stitching
        sorted_lookup: Dict[Tuple[int, int], Tile] = {
            (tile.x, tile.y): tile for tile in sorted_tiles
        }

        # Stitch tiles into a final image
        final_image = Image.new("RGB", (total_width, total_height))
        for x in range(top_left_quadkey.x, bottom_right_quadkey.x + 1):
            for y in range(top_left_quadkey.y, bottom_right_quadkey.y + 1):
                tile = sorted_lookup[(x, y)]
                tile_image = Image.open(tile.file_path)

                x_offset = (x - top_left_quadkey.x) * tile_width
                y_offset = (y - top_left_quadkey.y) * tile_height

                final_image.paste(tile_image, (x_offset, y_offset))
                tile_image.close()

        # Export output image as tiff
        final_image_path = os.path.join(download_folder_path, f"{aoi.id}.tiff")
        final_image.save(final_image_path, quality=100)
        final_image.close()
        self.file_path = final_image_path

        # Get corner coordinates
        upper_left_x, upper_left_y = aoi.envelope[0], aoi.envelope[3]
        lower_right_x, lower_right_y = aoi.envelope[1], aoi.envelope[2]

        # Open output image as raster
        final_image_raster = gdal.Open(final_image_path, gdal.GA_ReadOnly)

        # Create a new transformation
        geo_transform = [
            upper_left_x,
            (lower_right_x - upper_left_x) / final_image_raster.RasterXSize,
            0,
            upper_left_y,
            0,
            (lower_right_y - upper_left_y) / final_image_raster.RasterYSize,
        ]

        # Open the image file in write mode
        final_image_raster = gdal.Open(final_image_path, gdal.GA_Update)

        # Set the new geotransform and projection
        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromEPSG(4326)
        final_image_raster.SetGeoTransform(geo_transform)
        final_image_raster.SetProjection(spatial_reference.ExportToWkt())

        # Close driver
        final_image_raster = None
