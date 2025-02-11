from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status 
from ..service import auth as auth_service
from ..response.Token import Token
from ..request.RefreshTokenRequest import RefreshTokenRequest
from ..response.RefreshTokenResponse import RefreshTokenResponse
import jwt

router = APIRouter()

@router.post("/token", tags=['Auth'], description="Authentication route")
async def get_access_token(
    request: Annotated[OAuth2PasswordRequestForm, Depends()] 
) -> Token:
    
    user = auth_service.authenticate_user(request.username, request.password) 
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    response = auth_service.create_token(user.username, user.role)
    
    return response

@router.post("/refresh-token", tags=['Auth'], description="Access token refresh route")
async def refresh_access_token(
    request: RefreshTokenRequest
) -> RefreshTokenResponse:

    try:
        response = auth_service.create_new_access_token(request.refresh_token)
        return response

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")