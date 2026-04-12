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
    Accept two zip file uploads (boundary shapefile + election shapefile).
    Returns column names, feature count, and GeoJSON preview for the map.
    TODO: implement
    """
    pass
