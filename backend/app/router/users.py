from fastapi import APIRouter 
from typing import Annotated, Sequence
from fastapi import Depends, APIRouter, HTTPException, status 
from ..service import users as users_service
from ..service import auth as auth_service
from ..model.User import User
from ..request.UserCreate import UserCreate
from ..request.PasswordUpdate import PasswordUpdate
from ..common.UserBase import UserBase
from sqlalchemy.exc import IntegrityError
from ..service.auth import get_current_active_user, get_admin_user, SessionDep

router = APIRouter()
    
@router.get("/user/me/", tags=['User'], description="Route for getting info about the current active user")
async def get_my_user_info(
    current_user: Annotated[UserBase, Depends(get_current_active_user)] 
) -> User:
    
    return current_user

@router.put("/user", tags=['User'], description="Route for creating a a new user")
async def create_user(
    _: Annotated[UserBase, Depends(get_admin_user)],
    user: UserCreate, 
    session: SessionDep
):
    
    try:
        users_service.create_new_user(session, user) 
        return

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )
        
@router.post("/user", tags=['User'], description="Route for editing an existing user")
async def edit_user(
    _: Annotated[UserBase, Depends(get_admin_user)],
    user: UserCreate, 
    session: SessionDep
):
    
    try:
        users_service.update_user(user.id, user.username, user.fullname, user.role, session)
        return 
 
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists"
        )
        
@router.get("/user/all", tags=['User'], description="Route for retrieving a list with all users")
async def get_all_users(
    session: SessionDep, 
    _: Annotated[UserBase, Depends(get_admin_user)]
) -> Sequence[User]:

    response = users_service.get_all_users(session) 
    return response
    
@router.get("/user", tags=['User'], description="Route for creatina a new user")
async def delete_user(
    user_id : int,
    session: SessionDep, 
    _: Annotated[UserBase, Depends(get_admin_user)]
):
    
    users_service.delete_user(user_id, session)
    return 
        
@router.get("/user/toggle", tags=['User'], description="Route for disabling or enabling a user")
async def toggle_user(
    user_id : int,
    session: SessionDep, 
    _: Annotated[UserBase, Depends(get_admin_user)]
):
    
    users_service.toggle_user(user_id, session)
    return 
        
@router.post("/user/reset_password", tags=['User'], description="Route for password reset")
async def update_user_password(
    request : PasswordUpdate,
    session: SessionDep, 
    _: Annotated[UserBase, Depends(get_admin_user)]
):
    
    users_service.update_password(request.user_id, request.password, session)
    return  