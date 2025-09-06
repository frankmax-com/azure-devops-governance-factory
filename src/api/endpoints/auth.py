"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import structlog

from src.services.auth_service import AuthService
from src.models.auth import User, LoginRequest, TokenResponse

router = APIRouter()
security = HTTPBearer()
logger = structlog.get_logger(__name__)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, auth_service: AuthService = Depends()):
    """Authenticate user and return access token"""
    try:
        token = await auth_service.authenticate_user(request.username, request.password)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenResponse(
            access_token=token.access_token,
            token_type="bearer",
            expires_in=token.expires_in
        )
    except Exception as e:
        logger.error("Login failed", username=request.username, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/logout")
async def logout(token: str = Depends(security), auth_service: AuthService = Depends()):
    """Logout user and invalidate token"""
    try:
        await auth_service.invalidate_token(token.credentials)
        return {"message": "Successfully logged out"}
    except Exception as e:
        logger.error("Logout failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=User)
async def get_current_user(
    token: str = Depends(security),
    auth_service: AuthService = Depends()
):
    """Get current authenticated user"""
    try:
        user = await auth_service.get_current_user(token.credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error("Get current user failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


@router.post("/refresh")
async def refresh_token(
    token: str = Depends(security),
    auth_service: AuthService = Depends()
):
    """Refresh access token"""
    try:
        new_token = await auth_service.refresh_token(token.credentials)
        if not new_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenResponse(
            access_token=new_token.access_token,
            token_type="bearer",
            expires_in=new_token.expires_in
        )
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )
