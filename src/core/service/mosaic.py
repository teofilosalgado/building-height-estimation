from core.repository.aoi import get_aoi_repository
from core.repository.mosaic import get_mosaic_repository


def get_mosaics_by_feature_class():
    aoi_repository = get_aoi_repository()
    aois = aoi_repository.get_all()
    for aoi in aois:
        mosaic_repository = get_mosaic_repository()
        mosaic = mosaic_repository.get_by_aoi(aoi)
        yield mosaic
