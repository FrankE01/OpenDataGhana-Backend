from api.v1.router import dataset
from api.v1.router import tag
from fastapi import APIRouter

router = APIRouter()
router.include_router(dataset.router, prefix="/dataset", tags=["Dataset"])
router.include_router(tag.router, prefix="/tag", tags=["Tag"])
