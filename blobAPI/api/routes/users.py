from fastapi import APIRouter, HTTPException, status
from ..schema import User, db, UserResponse
from  ..utils import get_password_hashed
import secrets 
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    tags=["User Routes"]
)

@router.post("/signup", response_description="Register a user", response_model=UserResponse)
async def signup(user_info: User):
    user_info = jsonable_encoder(user_info)

    # check for duplicate
    username_found = await db["users"].find_one({"name":user_info["name"]})
    email_found = await db["users"].find_one({"email":user_info["email"]})

    if username_found:
        raise HTTPException(status.HTTP_409_CONFLICT, detail= "Username is already existed.")
    
    if email_found:
        raise HTTPException(status.HTTP_409_CONFLICT, detail= "email is already existed.")
    
    # hash user password
    user_info["password"] = get_password_hashed(user_info["password"])
    # create_apikey
    user_info["apikey"] = secrets.token_hex(30)
    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    # send email
    return created_user