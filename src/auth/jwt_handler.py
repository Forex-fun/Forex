from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import config

security = HTTPBearer()

class JWTHandler:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str):
        try:
            decoded_token = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
            return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
        except:
            return None
            
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        decoded_token = JWTHandler.decode_token(token)
        if decoded_token is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return decoded_token 