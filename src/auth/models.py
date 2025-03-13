from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    wallet_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0.0)
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            self.hashed_password.encode()
        )

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    wallet_address: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 