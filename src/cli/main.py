import click
from core.client import Bing
from core.client.virtual_earth import VirtualEarthMetadata
from core.service import geometry, image


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
    x = VirtualEarthMetadata(api_key)
    y = x.get_complete()
    z = x.get_basic(default_zoom_level, "-21,-43")
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
