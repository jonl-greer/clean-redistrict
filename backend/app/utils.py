import geopandas as gpd
import pandas as pd
from pathlib import Path
import zipfile
import tempfile
import os

def load_shapefile():
  """
  Accepts zipfile, extracts shapefiles, loads shapefiles with geopandas, reproject to common geography (EPSG:4269), returns GeoDataFrame
  """
  return
