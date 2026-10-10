from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, verify_token
from app.api import (
    auth_router,
    admin_router,
    candidate_profile_router,
    interview_router,
    question_router,
    candidate_answer_router,
    report_router,
    score_router,
    upload_router,
    resume_router,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.logger import setup_logging
from app.core.exceptions import register_exception_handlers

from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.process_time import ProcessTimeMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

import os
from app.api import tts
from app.api import speech_to_text
from app.api import vision

setup_logging()
app = FastAPI(
    title="AI Interview Assessment System API",
    version="1.0.0",
    description="Backend API for the AI-Powered Intelligent Video Interview Assessment System",
)
register_exception_handlers(app)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create uploads directories if they don't exist
os.makedirs("uploads/profile_images", exist_ok=True)
os.makedirs("uploads/resumes", exist_ok=True)

# Mount the uploads directory as static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Register routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(candidate_profile_router)
app.include_router(interview_router)
app.include_router(question_router)
app.include_router(candidate_answer_router)
app.include_router(report_router)
app.include_router(score_router)
app.include_router(upload_router)
app.include_router(resume_router)

app.include_router(tts.router)
app.include_router(speech_to_text.router)
app.include_router(vision.router)


@app.get("/")


def root():
    return {"message": "AI Interview Assessment System API is running 🚀"}


@app.get("/db-test")
def db_test():
    """
    Simple endpoint to verify that the application
    can successfully connect to PostgreSQL.
    """
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "Connected Successfully ✅"
    }




@app.get("/jwt")
def jwt_test():
    token = create_access_token(
        {"sub": "niraj@example.com"}
    )

    return {
        "access_token": token
    }


@app.get("/jwt-verify")
def jwt_verify():
    token = create_access_token(
        {"sub": "niraj@example.com"}
    )

    payload = verify_token(token)

    return payload


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "healthy"
    }