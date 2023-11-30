from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException
from typing import Optional


class SignUp(BaseModel):
    firstName: str
    lastName: str
    userName: str
    email: EmailStr
    password: str
    cPassword: str

    @validator('cPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise HTTPException(
                status_code=401, detail='Password do not match.')
        return v
    
    @validator("userName", pre=True, always=True)
    def strip_userName(cls, value):
        return value.strip()
    
    @validator("email", pre=True, always=True)
    def strip_email(cls, value):
        return value.strip()


class Login(BaseModel):
    userName: str
    password: str
    
    @validator("userName", pre=True, always=True)
    def strip_userName(cls, value):
        return value.strip()


class updateUser(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    userName: Optional[str]
    email: Optional[EmailStr]
    roles: Optional[str]
    password: str
