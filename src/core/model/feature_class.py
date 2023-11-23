from typing import List

from osgeo import gdal, ogr, osr

from core.model import AOI


class FeatureClass:
    def __init__(self, feature_class_path: str) -> None:
        self.file_path = feature_class_path
        self.spatial_reference = osr.SpatialReference()
        self.spatial_reference.ImportFromEPSG(4326)

        # Calculate AOIs from feature class
        aois: List[AOI] = []

        # Read input feature class
        input_feature_class = ogr.Open(self.file_path, gdal.OF_VECTOR)

        # Iterate over features
        input_layer = input_feature_class.GetLayer()
        for input_feature in input_layer:
            # Get feature properties
            id = int(input_feature.GetField("FID"))
            label = str(input_feature.GetField("LABEL"))
            # Get feature geometry, spatial reference and authority code
            input_geometry = input_feature.GetGeometryRef()
            input_spatial_reference = input_geometry.GetSpatialReference()
            input_authority_code = input_spatial_reference.GetAuthorityCode(None)

            # Checks if geometry spatial reference matches the default one
            if self.spatial_reference.GetAuthorityCode(None) != input_authority_code:
                # Apply transformation if they differ
                transform = osr.CoordinateTransformation(
                    input_spatial_reference,
                    self.spatial_reference,
                )
                input_geometry.Transform(transform)

            # Generate area of interest
            aois.append(AOI(id, label, input_geometry))
        self.aois = aois
