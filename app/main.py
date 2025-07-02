from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.models import AnomalyRequest, AnomalyResponse, HealthCheck
from app.ad_wrapper import run_anomaly_detection

app = FastAPI(
    title="Anomaly Detection API",
    description="FastAPI service to run LSTM-based Anomaly Detection on CSV sensor data",
    version="1.0.0"
)

@app.get("/", response_model=HealthCheck)
def root():
    return HealthCheck(status="running", timestamp=datetime.now(), version="1.0.0")

@app.get("/health", response_model=HealthCheck)
def health_check():
    return HealthCheck(status="healthy", timestamp=datetime.now(), version="1.0.0")

@app.post("/run_ad", response_model=AnomalyResponse)
def run_ad(request: AnomalyRequest):
    try:
        output_path = run_anomaly_detection(request.csv_path, request.device_type)
        return AnomalyResponse(
            message="Anomaly Detection completed successfully",
            output_path=output_path,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
