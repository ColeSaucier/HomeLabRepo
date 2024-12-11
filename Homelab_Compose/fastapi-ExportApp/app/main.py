from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from typing import Union
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class ExportRequest(BaseModel):
    time_begin: float
    time_end: float

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run-export-script")
async def run_export_script(request_data: ExportRequest):
    script_path = "/scripts/dbToCsv.py"
    logger.info(f"Attempting to run script at path: {script_path} with parameters: {request_data}")
    logger.info(f"Received data: {request_data}")
    
    # Prepare environment variables for the script
    env = os.environ.copy()
    env['TIME_BEGIN'] = str(request_data.time_begin)
    env['TIME_END'] = str(request_data.time_end)

    try:
        # Run the script with environment variables, capturing both stdout and stderr
        result = subprocess.run(["python", script_path], capture_output=True, text=True, env=env)
        logger.info(f"Script stdout: {result.stdout}")
        logger.info(f"Script stderr: {result.stderr}")
        logger.info(f"Script return code: {result.returncode}")
        
        if result.returncode != 0:
            logger.error(f"Script execution failed with return code {result.returncode}")
            raise HTTPException(status_code=500, detail=f"Script execution failed: {result.stderr}")
        
        return {"message": "Export completed successfully", "output": result.stdout}
    
    except Exception as e:
        logger.exception("An error occurred while running the export script")
        raise HTTPException(status_code=500, detail=str(e))
