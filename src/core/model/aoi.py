from osgeo.ogr import Geometry


class AOI:
    def __init__(
        self,
        id: int,
        label: str,
        geometry: Geometry,
    ) -> None:
        self.id = id
        self.label = label

        self.envelope = geometry.GetEnvelope()

        x = geometry.Centroid().GetX()
        y = geometry.Centroid().GetY()
        self.centroid = (x, y)
