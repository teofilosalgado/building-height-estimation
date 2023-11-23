import click
from core.service.mosaic import get_mosaics_by_feature_class


@click.command()
@click.argument("input_feature_class_path", type=click.Path())
def main(input_feature_class_path: str):
    result = list(get_mosaics_by_feature_class(input_feature_class_path))

    print("Done")


if __name__ == "__main__":
    main()
