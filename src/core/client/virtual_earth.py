from typing import List

from uplink import Consumer, Path, Query, get, returns

from core.dto.virtual_earth import BasicMetadata, CompleteMetadata, ResourceSet


class VirtualEarthMetadata(Consumer):
    base_url = "https://dev.virtualearth.net/REST/V1/Imagery/"

    def __init__(self, api_key: str):
        super(VirtualEarthMetadata, self).__init__(self.base_url)
        self._inject(Query("key").with_value(api_key))

    @returns.json(key="resourceSets")
    @get("Metadata/Aerial")
    def get_complete(self) -> List[ResourceSet[CompleteMetadata]]:  # type: ignore
        """Get user's public repositories."""

    @returns.json(key="resourceSets")
    @get("Metadata/Aerial/{center_point}", args=(Query, Path))
    def get_basic(self, zl: int, center_point: str) -> List[ResourceSet[BasicMetadata]]:  # type: ignore
        """Get user's public repositories."""
