import motor.motor_asyncio
from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
import os

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URI"))

db = client.music_api

#BSON and fastapi #JSON
class PyObjectID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
    
class User(BaseModel):
    # id: PyObjectID = Field(default_factory=PyObjectID, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoder = {ObjectId: str}
        schema_extra = {
            "example" : {
                "name" : "John Doe",
                "email" : "jdoe@example.com",
                "password" : "secret_code"
            }
        }

class UserResponse(BaseModel):
    id: PyObjectID = Field(default_factory=PyObjectID, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)

    class config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example" : {
                "name" : "John Doe",
                "email" : "jdoe@example.com"
            }
        }