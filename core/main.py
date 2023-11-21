from datetime import datetime

import click
from clients import Bing
from services.geometry import get_envelope_from_feature


def get_iso8601():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


@click.command()
@click.argument("api_key")
@click.argument("default_zoom_level", type=int)
@click.argument("input_feature_class_path")
@click.argument("download_folder_path")
def main(
    api_key: str,
    default_zoom_level: int,
    input_feature_class_path: str,
    download_folder_path: str,
):
    # Default imagery client
    client = Bing(default_zoom_level, download_folder_path, 4326, api_key)

    # Create one building object per feature
    get_envelope_from_feature(input_feature_class_path, client.spatial_reference)

    tiles = client.download_tiles_from_envelope(*envelope)
    image.merge_tiles(tiles, client.image_height, client.image_width)
    pass


if __name__ == "__main__":
    main()
