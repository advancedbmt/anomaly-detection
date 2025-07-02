from pydantic import BaseModel
from datetime import datetime

class AnomalyRequest(BaseModel):
    csv_path: str
    device_type: str

class AnomalyResponse(BaseModel):
    message: str
    output_path: str
    timestamp: datetime

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
