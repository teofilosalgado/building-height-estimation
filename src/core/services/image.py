import os
from typing import Dict, Iterable, Tuple

from PIL import Image

from core.clients import Base
from core.models import AOI, Mosaic, Tile


def generate_mosaic_from_aoi(client: Base, aoi: AOI):
    tiles = client.download_tiles_from_envelope(*aoi.envelope)
    image_date = client.get_imagery_date_from_centroid(*aoi.centroid)
    image_path = _merge_tiles(
        client.image_height, client.image_width, client.download_folder_path, aoi, tiles
    )
    return Mosaic(aoi, tiles, image_date, image_path)


def _merge_tiles(
    tile_height: int,
    tile_width: int,
    download_folder_path: str,
    aoi: AOI,
    tiles: Iterable[Tile],
):
    # Sort tiles from top left to bottom right
    sorted_tiles = sorted(tiles, key=lambda item: [item.y, item.x])

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
            tile_image = Image.open(tile.image_path)

            x_offset = (x - top_left_quadkey.x) * tile_width
            y_offset = (y - top_left_quadkey.y) * tile_height

            final_image.paste(tile_image, (x_offset, y_offset))
            tile_image.close()

    # Full quality on the output image
    final_image_path = os.path.join(download_folder_path, f"{aoi.id}.jpeg")
    final_image.save(final_image_path, quality=100)
    final_image.close()
    return final_image_path
