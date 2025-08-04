import random
from datetime import timedelta

import httpx
from fastapi import Request, Response, HTTPException, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from shared.config import settings
from shared.dynamodb import get_table
from shared.logger import get_logger

logger = get_logger("user-management-service")
app = FastAPI()
router = APIRouter()

# Temporary in-memory store
otp_store = {}

origins = ["*"]  # Allow all for dev/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str


class EmailRequest(BaseModel):
    email: str


class OTPVerifyRequest(BaseModel):
    email: str
    otp: int


@app.post("/api/auth/start")
def start_auth(req: LoginRequest):
    print(f"request email {req.email}")
    if req.email.endswith("@gmail.com"):
        sso_login_url = (
            f"{settings.cognito_domain}/oauth2/authorize"
            f"?response_type=code"
            f"&client_id={settings.cognito_client_id}"
            f"&redirect_uri={settings.cognito_redirect_uri}"
            f"&scope=openid"
            f"&identity_provider={settings.cognito_identity_provider}"
            f"&login_hint={req.email}"
        )
        return {"method": "sso", "redirect_url": sso_login_url}
    else:
        otp_store[req.email] = random.randint(100000, 999999)
        print(f"Generated OTP for {req.email}: {otp_store[req.email]}")
        return {"method": "otp"}


@app.post("/api/auth/resend-otp")
def resend_otp(req: EmailRequest):
    if req.email not in otp_store:
        raise HTTPException(status_code=400, detail="Email not found. Please initiate login first.")

    # Resend simulated
    otp_store[req.email] = random.randint(100000, 999999)
    print(f"Resent OTP for {req.email}: {otp_store[req.email]}")
    return {"status": "ok", "message": "OTP resent successfully"}


@app.post("/api/auth/verify-otp")
def verify_otp(req: OTPVerifyRequest):
    stored_otp = otp_store.get(req.email)
    print(stored_otp)

    if not stored_otp:
        raise HTTPException(status_code=400, detail="Email not recognized. Please request OTP again.")

    if req.otp != stored_otp:
        raise HTTPException(status_code=401, detail="Invalid OTP.")

    # OTP verified, simulate login success
    print(f"OTP verified for {req.email}")
    return {
        "status": "success",
        "message": "OTP verified successfully",
        "access_token": "mocked-jwt-token",
        "user": {"email": req.email}
    }


@router.get("/api/auth/callback")
async def cognito_callback(request: Request, response: Response, code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    token_url = f"{settings.cognito_domain}/oauth2/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.cognito_client_id,
        "redirect_uri": settings.cognito_redirect_uri,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # # Basic Auth header
    # auth = (settings.cognito_client_id, settings.cognito_client_secret)
    #
    # async with httpx.AsyncClient() as client:
    #     token_res = await client.post(token_url, data=payload, headers=headers, auth=auth)

    async with httpx.AsyncClient() as client:
        token_res = await client.post(token_url, data=payload, headers=headers)

    if token_res.status_code != 200:
        print("Cognito token error:", token_res.text)
        raise HTTPException(status_code=400, detail="Failed to exchange code for token")

    tokens = token_res.json()
    access_token = tokens.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token received")

    # Set token in secure HttpOnly cookie
    resp = RedirectResponse(url=settings.cognito_frontend_url, status_code=302)
    resp.set_cookie(
        key="access_token",
        value=access_token,
        max_age=int(timedelta(hours=1).total_seconds()),
        httponly=True,
        secure=True,
        samesite="Lax",
        path="/"
    )
    return resp


@router.get("/api/auth/logout")
def logout_user():
    cognito_logout_url = (
        f"{settings.cognito_domain}/logout"
        f"?client_id={settings.cognito_client_id}"
        f"&logout_uri={settings.cognito_logout_redirect_uri}"
    )

    # Optionally delete cookies
    response = RedirectResponse(url=cognito_logout_url, status_code=302)
    response.delete_cookie("access_token", path="/")
    return response


@router.get("/api/auth/me")
async def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    userinfo_url = f"{settings.cognito_domain}/oauth2/userInfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(userinfo_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token or session expired")

    return response.json()


app.include_router(router)


@app.get("/")
def get_users():
    logger.info("GET / called")
    return {"message": "Hello, Get users for user management with logger!"}


@app.get("/env")
def get_env_details():
    return {
        "environment": settings.app_env,
        "log_level": settings.log_level,
        "dynamodb_table": settings.dynamodb_table_name,
        "endpoint": settings.dynamodb_endpoint,
    }


@app.get("/health/dynamodb")
async def test_dynamodb_connection():
    try:
        table = get_table()
        # This will call DescribeTable behind the scenes
        table.load()
        return {"status": "success", "table": table.table_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB connection failed: {str(e)}")
