import geopandas as gpd
import pandas as pd
from pathlib import Path
import zipfile
import tempfile
import os

def load_shapefile(zip_bytes: bytes, target_crs: str = "EPSG:4269") -> gpd.GeoDataFrame:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "upload.zip"
        zip_path.write_bytes(zip_bytes)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmpdir)

        shp_files = list(Path(tmpdir).rglob("*.shp"))
        if not shp_files:
            raise ValueError("No .shp file found in the uploaded zip archive")

        gdf = gpd.read_file(shp_files[0])

        if gdf.crs is None or gdf.crs.to_epsg() != int(target_crs.split(":")[1]):
            gdf = gdf.to_crs(target_crs)

        return gdf
