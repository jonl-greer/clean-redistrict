from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import json
from .utils import load_shapefile

router = APIRouter()

@router.post("/upload")
async def upload_files(
    boundary: UploadFile = File(...),
    election: UploadFile = File(...)
):
    try:
        boundary_bytes = await boundary.read()
        election_bytes = await election.read()

        boundary_gdf = load_shapefile(boundary_bytes)
        election_gdf = load_shapefile(election_bytes)

        return JSONResponse({
            "boundary": {
                "columns": list(boundary_gdf.columns),
                "row_count": len(boundary_gdf),
                "geojson": json.loads(boundary_gdf.to_json()),
            },
            "election": {
                "columns": list(election_gdf.columns),
                "row_count": len(election_gdf),
            },
        })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
