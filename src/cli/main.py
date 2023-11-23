from core.service.mosaic import get_mosaics_by_feature_class


def main():
    result = list(get_mosaics_by_feature_class())

    print("Done")


if __name__ == "__main__":
    main()
