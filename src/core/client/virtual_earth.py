from typing import List

from requests import Response
from uplink import Consumer, Path, Query, get, returns

from core.dto.virtual_earth import BasicMetadata, CompleteMetadata, ResourceSet


class VirtualEarthMetadataClient(Consumer):
    base_url = "https://dev.virtualearth.net/REST/V1/Imagery/Metadata/"

    def __init__(self, api_key: str):
        super(VirtualEarthMetadataClient, self).__init__(self.base_url)
        self._inject(Query("key").with_value(api_key))

    @returns.json(key="resourceSets")
    @get("Aerial")
    def get_complete(self) -> List[ResourceSet[CompleteMetadata]]:  # type: ignore
        pass

    @returns.json(key="resourceSets")
    @get("Aerial/{center_point}", args=(Query("zl"), Path))
    def get_basic(
        self, zoom_level: int, center_point: str
    ) -> List[ResourceSet[BasicMetadata]]:  # type: ignore
        pass


class VirtualEarthTileClient(Consumer):
    def __init__(self, base_url: str, generation: int):
        super(VirtualEarthTileClient, self).__init__(base_url)
        self._inject(Query("g").with_value(generation))

    @get("tiles/a{quadkey}.jpeg", args=(Path,))
    def get(self, quadkey: str) -> Response:  # type: ignore
        pass
