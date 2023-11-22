from datetime import datetime

import click
from core.clients import Bing
from core.services import geometry, image


def get_iso8601():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


@click.command()
@click.argument("api_key")
@click.argument("default_zoom_level", type=int)
@click.argument("download_folder_path")
@click.argument("input_feature_class_path")
def main(
    api_key: str,
    default_zoom_level: int,
    input_feature_class_path: str,
    download_folder_path: str,
):
    # Default imagery client
    client = Bing(api_key, default_zoom_level, download_folder_path)

    # Get all areas of interest from feature class
    aois = geometry.get_aois_from_feature_class(
        client.spatial_reference,
        input_feature_class_path,
    )

    # Download image mosaics for each aoi
    mosaics = [image.generate_mosaic_from_aoi(client, aoi) for aoi in aois]

    print("Done")


if __name__ == "__main__":
    main()
