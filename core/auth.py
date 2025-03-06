from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core import supabase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")

async def verify_user(token: str = Depends(oauth2_scheme)):
    try:
        response = supabase.auth.get_user(token)
        return response

    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)