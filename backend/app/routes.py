from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import json

@router.post("/upload")
async def upload_files(
    boundary: UploadFile = File(...),
    election: UploadFile = File(...)
):
    """
    Accepts two zip files, calls load_shapefile function for each, returns column names, # of rows, GeoJSON of boundary file
    """
    pass
