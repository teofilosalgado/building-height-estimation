from osgeo.ogr import Geometry

from core.model.envelope import Envelope


class AOI:
    def __init__(
        self,
        id: int,
        label: str,
        geometry: Geometry,
    ) -> None:
        self.id = id
        self.label = label

        self.envelope = Envelope(*geometry.GetEnvelope())

        x = geometry.Centroid().GetX()
        y = geometry.Centroid().GetY()
        self.centroid = (x, y)
