from osgeo import gdal, ogr, osr
from osgeo.osr import SpatialReference


def get_envelope_from_feature(
    input_feature_class_path: str, output_spatial_reference: SpatialReference
):
    # Read input feature class
    input_feature_class = ogr.Open(input_feature_class_path, gdal.OF_VECTOR)

    # Iterate over features
    input_layer = input_feature_class.GetLayer()
    for input_feature in input_layer:
        # Get feature properties
        id = input_feature.GetField("FID")
        label = input_feature.GetField("LABEL")
        # Get feature geometry, spatial reference and authority code
        input_geometry = input_feature.GetGeometryRef()
        input_spatial_reference = input_geometry.GetSpatialReference()
        input_authority_code = input_spatial_reference.GetAuthorityCode(None)

        # Checks if geometry spatial reference matches the default one
        if output_spatial_reference.GetAuthorityCode(None) != input_authority_code:
            # Apply transformation if they differ
            transform = osr.CoordinateTransformation(
                input_spatial_reference,
                output_spatial_reference,
            )
            input_geometry.Transform(transform)

        # Get geometry envelope
        envelope = input_geometry.GetEnvelope()
