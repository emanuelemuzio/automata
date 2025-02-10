import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer 
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound 
from jwt.exceptions import InvalidTokenError
from ..model.User import User
from ..config import *
from ..db import *
from ..response.RefreshTokenResponse import RefreshTokenResponse
from ..response.Token import Token
from ..common.TokenData import TokenData
from ..common.UserBase import UserBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password : str) -> str:
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> User | bool:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.pwd):
        return False
    return user

def get_user(username: str) -> User:
    try:
        statement = select(User).where(User.username == username)
        with Session(engine) as session:
            res = session.exec(statement).one()
        return res
    
    except NoResultFound: 
        print("No result found")
        
    except MultipleResultsFound:
        print("Multiple results found")
        
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_admin_user(
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    if current_user.role != 'ADMIN':
        raise HTTPException(status_code=401, detail="Not an admin user")
    return current_user

def create_token(username : str, role : str) -> Token:
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username, "role" : role}, expires_delta=access_token_expires
    )
    
    refresh_token = create_access_token({"sub": username, "role" : role}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    
    token = Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
    
    return token

def create_new_access_token(refresh_token : str):
    
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    new_access_token_obj = RefreshTokenResponse(access_token=new_access_token, token_type="bearer")
    
    return new_access_token_obj

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt