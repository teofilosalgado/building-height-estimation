from core.model import FeatureClass
from core.repository.mosaic import get_mosaic_repository


def get_mosaics_by_feature_class(input_feature_class_path: str):
    feature_class = FeatureClass(input_feature_class_path)
    for aoi in feature_class.aois:
        mosaic = get_mosaic_repository().get_by_aoi(aoi)
        yield mosaic
