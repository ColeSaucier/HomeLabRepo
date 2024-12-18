from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
import subprocess
import os
import logging
from datetime import date, datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/app/logs/app.log',
    filemode='a'
)
logger = logging.getLogger(__name__)
from typing import Union
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class ExportRequest(BaseModel):
    time_begin: date
    time_end: date

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()  # Serialize date to ISO format
        }

@app.get("/")
async def read_root(request: Request):
    # Use date.today() instead of datetime.now()
    default_time_begin = (date.today() - timedelta(days=14)).isoformat()
    default_time_end = date.today().isoformat()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "default_time_begin": default_time_begin,
        "default_time_end": default_time_end
    })

@app.post("/run-export-script")
async def run_export_script(request_data: ExportRequest):
    script_path = "/scripts/dbToCsv.py"
    logger.info(f"Attempting to run script at path: {script_path} with parameters: {request_data}")
    logger.info(f"Received data: {request_data}")
    
    # Prepare environment variables for the script
    env = os.environ.copy()
    # Convert date to datetime with min/max time for timestamps
    env['TIME_BEGIN'] = str(int(datetime.combine(request_data.time_begin, datetime.min.time()).timestamp()))
    env['TIME_END'] = str(int(datetime.combine(request_data.time_end, datetime.max.time()).timestamp()))

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
