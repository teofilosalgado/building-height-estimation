import click
from core.service.mosaic import get_mosaics_by_feature_class
from core.service.shadow import get_mask_by_mosaic


@click.command()
@click.argument("input_feature_class_path", type=click.Path())
def main(input_feature_class_path: str):
    for mosaic in get_mosaics_by_feature_class(input_feature_class_path):
        mask = get_mask_by_mosaic(mosaic)
        print(mask.mosaic.aoi.id)

    print("Done")


if __name__ == "__main__":
    main()
