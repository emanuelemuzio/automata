from fastapi import APIRouter
from typing import Annotated, Sequence
from fastapi import Depends, APIRouter, File, UploadFile
from ..service import documents as documents_service
from ..service.auth import *
from ..common.UserBase import UserBase
from ..model.Document import Document
from fastapi.responses import FileResponse

router = APIRouter()

@router.put("/document", tags=['Document'], description="Route for document upload")
async def upload_document(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    file: Annotated[UploadFile, File()],
    session: SessionDep
):
    documents_service.document_upload(file, current_user.id, session)
    return
        
@router.get("/document/by_user", tags=['Document'], description="Route for retrieving documents uploaded by authenticated user")
async def get_user_documents(
    session: SessionDep,
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
) -> Sequence[Document]:
    
    response = documents_service.get_user_documents(current_user.id, session)
    return response

@router.get("/document/download", tags=['Document'], description="Route for downloading a specific document")
async def download_document(
    document_id: int, 
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    session: SessionDep,
) -> FileResponse:
    
    response = documents_service.download(document_id, current_user.id, session)
    return response

@router.delete("/document")
async def delete_user(
    document_id : int,
    session: SessionDep, 
    vector_session: VecSessionDep, 
    current_user: UserBase = Depends(get_current_active_user)
): 
    
    documents_service.delete(document_id, current_user.id, session, vector_session)
    return 