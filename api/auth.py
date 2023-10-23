from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
from config import AppConfig

api_key_header = APIKeyHeader(name=AppConfig.Auth.API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == AppConfig.Auth.API_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, 
            detail="Invalid API Key"
        )
    
APIKeyValidation = Depends(validate_api_key)