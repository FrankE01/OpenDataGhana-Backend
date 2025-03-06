from fastapi import APIRouter

from api.v1.router import dataset, tag, user

router = APIRouter()

router.include_router(dataset.router, prefix="/dataset", tags=["Dataset"])
router.include_router(tag.router, prefix="/tag", tags=["Tag"])
router.include_router(user.router, prefix="/user", tags=["User"])
