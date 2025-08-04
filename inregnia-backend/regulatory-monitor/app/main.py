from fastapi import FastAPI
from shared.logger import get_logger

logger = get_logger("regulatory-monitor-service")
app = FastAPI()


@app.get("/")
def get_documents():
    logger.info("GET / called")
    return {"message": "Hello, Get documents for regulatory monitor with logger!"}
