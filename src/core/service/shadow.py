import gc
import json
import os

import cv2
import numpy as np
import pandas as pd
import rasterio
from osgeo import ogr
from rasterio.features import shapes
from settings import get_settings
from skimage.color import lab2lch, rgb2lab
from skimage.exposure import rescale_intensity
from skimage.morphology import disk
from sklearn.cluster import KMeans

from core.model import Mask, Mosaic


def get_mask_by_mosaic(
    mosaic: Mosaic,
    convolve_window_size=3,
    number_of_thresholds=1,
    disk_radius=1,
):
    """
    This function is used to detect shadow - covered areas in an image, as proposed in the paper
    'Near Real - Time Shadow Detection and Removal in Aerial Motion Imagery Application' by Silva G.F., Carneiro G.B.,
    Doth R., Amaral L.A., de Azevedo D.F.G. (2017)

    Parameters:
    - convolve_window_size: Size of convolutional matrix filter to be used for blurring of specthem ratio image
    - number_of_thresholds: Number of thresholds to be used for automatic multilevel global threshold determination
    - disk_radius: Size of disk - shaped structuring element to be used for morphological closing operation

    """

    if convolve_window_size % 2 == 0:
        raise ValueError("Please make sure that convolve_window_size is an odd integer")

    with rasterio.open(mosaic.file_path) as f:
        metadata = f.profile
        img = rescale_intensity(
            np.transpose(f.read(tuple(np.arange(metadata["count"]) + 1)), [1, 2, 0]),
            out_range="uint8",
        )
        img = img[:, :, 0:3]

    lch_img = np.float32(lab2lch(rgb2lab(img)))

    l_norm = rescale_intensity(lch_img[:, :, 0], out_range=(0, 1))
    h_norm = rescale_intensity(lch_img[:, :, 2], out_range=(0, 1))
    sr_img = (h_norm + 1) / (l_norm + 1)
    log_sr_img = np.log(sr_img + 1)

    del l_norm, h_norm, sr_img
    gc.collect()

    avg_kernel = np.ones((convolve_window_size, convolve_window_size)) / (
        convolve_window_size**2
    )
    blurred_sr_img = cv2.filter2D(log_sr_img, ddepth=-1, kernel=avg_kernel)

    del log_sr_img
    gc.collect()

    flattened_sr_img = blurred_sr_img.flatten().reshape((-1, 1))
    labels = (
        KMeans(n_clusters=number_of_thresholds + 1, n_init="auto", max_iter=10000)
        .fit(flattened_sr_img)
        .labels_
    )
    flattened_sr_img = flattened_sr_img.flatten()
    df = pd.DataFrame({"sample_pixels": flattened_sr_img, "cluster": labels})
    threshold_value = df.groupby(["cluster"]).min().max()[0]
    df["Segmented"] = np.uint8(df["sample_pixels"] >= threshold_value)

    del blurred_sr_img, flattened_sr_img, labels, threshold_value
    gc.collect()

    shadow_mask_initial = np.array(df["Segmented"]).reshape(
        (img.shape[0], img.shape[1])
    )
    struc_elem = disk(disk_radius)
    shadow_mask = np.expand_dims(
        np.uint8(cv2.morphologyEx(shadow_mask_initial, cv2.MORPH_CLOSE, struc_elem)),
        axis=0,
    )

    del df, shadow_mask_initial, struc_elem
    gc.collect()

    metadata["count"] = 1
    shadow_mask_file_name = f"{mosaic.aoi.id}-masked.tiff"
    shadow_mask_file_path = os.path.join(
        get_settings().download_folder_path, shadow_mask_file_name
    )
    with rasterio.open(shadow_mask_file_path, "w", **metadata) as dst:
        dst.write(shadow_mask)
        geojson_shadows = [
            shape[0]
            for shape in shapes(shadow_mask, transform=dst.transform)
            if shape[1]
        ]
    geometry_shadows = [
        ogr.CreateGeometryFromJson(json.dumps(geojson)) for geojson in geojson_shadows
    ]
    largest_geometry_shadow = max(geometry_shadows, key=lambda item: item.GetArea())
    simplified_largest_geometry_shadow = largest_geometry_shadow.Simplify(0.000005)

    linear_ring = simplified_largest_geometry_shadow.GetGeometryRef(0)
    vertex_count = linear_ring.GetPointCount()
    vertices = [linear_ring.GetPoint(i) for i in range(vertex_count)]
    rightmost_vertex = max(vertices, key=lambda item: item[0])
    bottommost_vertex = min(vertices, key=lambda item: item[1])
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(rightmost_vertex[0], rightmost_vertex[1])
    line.AddPoint(bottommost_vertex[0], bottommost_vertex[1])
    result = line.ExportToJson()
    with open(f"{mosaic.aoi.id}.json", "w", encoding="utf-8") as file:
        file.write(result)

    return Mask(mosaic, shadow_mask_file_path, simplified_largest_geometry_shadow)
