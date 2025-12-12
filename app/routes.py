from fastapi import APIRouter, HTTPException, status
from typing import List
from pymongo.errors import DuplicateKeyError
from app.schemas import UserCreate, UserOut, UserUpdate,UserDelete
from app import service2

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: UserCreate):
    try:
        user = service2.create_user(payload)
        return user
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")

@router.get("", response_model=List[UserOut])
def list_users_endpoint():
    return service2.list_users()

@router.get("/{id}", response_model=UserOut)
def get_user_endpoint(id: str):
    user = service2.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/update-password", response_model=UserOut)
def update_password_endpoint(payload: UserUpdate):
    updated = service2.update_password(payload)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("", status_code=status.HTTP_202_ACCEPTED)
def delete_user_endpoint(payload:UserDelete):
    ok = service2.delete_user(payload)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return
