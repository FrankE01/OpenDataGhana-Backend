from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from core import logger, supabase
from schema import UserModel

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Use this endpoint to login
    """
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": form_data.username, "password": form_data.password}
        )

        return {"access_token": response.session.access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/register")
async def register(form_data: UserModel):
    """
    Use this endpoint to register
    """
    try:
        response = supabase.auth.sign_up(
            {
                "email": form_data.email,
                "password": form_data.password,
                "options": {"data": {"username": form_data.username}},
            }
        )

        return {
            "details": {
                "message": "User created successfully",
                "email": response.user.email,
                "confirmation_sent_at": response.user.confirmation_sent_at,
            }
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/resend-verification")
async def resent_verification(email: str):
    """
    Use this endpoint to resend verification
    """
    try:
        response = supabase.auth.resend({"email": email, "type": "signup"})
        return {"details": {"message": "Verification email sent successfully"}}

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
