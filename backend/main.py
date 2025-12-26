import os
from typing import Dict, Any, Union, List
from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import tempfile
import uuid
import mimetypes
import ezdxf

# Ensure absolute paths relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
assets_dir = os.path.join(static_dir, "assets")

from .interfaces.dxf_generator_interface import DXFGeneratorInterface
from .services.dxf_service import DXFService
from .interfaces.validator import Validator

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Fix for Windows MIME types
mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/vite.svg")
async def read_vite_svg():
    return FileResponse(os.path.join(static_dir, "vite.svg"))

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.post("/parse-dxf")
async def parse_dxf(file: UploadFile = File(...)):
    """
    Parses an uploaded DXF file to extract parameters.
    """
    if not file.filename.lower().endswith('.dxf'):
        raise HTTPException(status_code=400, detail="Only DXF files are allowed")

    tmp_path = None
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="File is empty")
            tmp.write(content)
            tmp_path = tmp.name

        doc = ezdxf.readfile(tmp_path)
        msp = doc.modelspace()
        
        polylines = msp.query('LWPOLYLINE')
        if not polylines:
            raise HTTPException(status_code=400, detail="No polyline found in DXF")
        
        pline = polylines[0]
        points = pline.get_points()
        num_points = len(points)

        if num_points == 12:
            coords = [(p[0], p[1]) for p in points]
            xs = [p[0] for p in coords]
            ys = [p[1] for p in coords]
            H = max(ys) - min(ys)
            B = max(xs) - min(xs)
            tf = abs(coords[0][1] - coords[11][1])
            tw = abs(coords[3][0] - coords[10][0])
            return {
                "type": "beam",
                "params": {"H": round(H, 2), "B": round(B, 2), "tw": round(tw, 2), "tf": round(tf, 2)}
            }
        elif num_points == 4:
            coords = [(p[0], p[1]) for p in points]
            xs = [p[0] for p in coords]
            ys = [p[1] for p in coords]
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)
            return {
                "type": "column",
                "params": {"width": round(width, 2), "height": round(height, 2)}
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported polyline structure ({num_points} points)")

    except ezdxf.DXFError as e:
        raise HTTPException(status_code=400, detail=f"Invalid DXF file: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error parsing DXF: {str(e)}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

class GenerateRequest(BaseModel):
    component_type: str
    params: Dict[str, float]

@app.post("/generate")
def generate_dxf(request: GenerateRequest, background_tasks: BackgroundTasks):
    try:
        if request.component_type == "beam":
            is_valid, error_msg = Validator.validate_beam(request.params)
            if not is_valid: raise HTTPException(status_code=400, detail=error_msg)
        elif request.component_type == "column":
             is_valid, error_msg = Validator.validate_column(request.params)
             if not is_valid: raise HTTPException(status_code=400, detail=error_msg)
        else:
            raise HTTPException(status_code=400, detail="Invalid component type")

        dxf_service = DXFService()
        generated_filename = f"{uuid.uuid4()}.dxf"
        tmp_path = os.path.join(tempfile.gettempdir(), generated_filename)
        
        generator = DXFGeneratorInterface(request.component_type, request.params)
        component = generator.get_component()
        saved_file = dxf_service.save(component, filename=tmp_path)
        
        background_tasks.add_task(os.remove, saved_file)
        return FileResponse(path=saved_file, filename=f"{request.component_type}.dxf", media_type='application/dxf')

    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
