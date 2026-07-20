from fastapi import APIRouter, Depends
from typing import List

from app.core.config import config
from app.services.anytype_service import AnyTypeService
from app.schemas.anytype import AnyTypeSpace

router = APIRouter(prefix="/anytype", tags=["AnyType"])

def get_anytype_service() -> AnyTypeService:
    """
    Dependency function to provide an instance of AnyTypeService.
    This allows for easier testing and potential future enhancements.
    """
    return AnyTypeService(
        base_url=config.anytype_base_url,
        api_key=config.anytype_api_key
    )

@router.get("/spaces", response_model=List[AnyTypeSpace])
def show_spaces(service: AnyTypeService = Depends(get_anytype_service)):
    spaces = service.get_spaces().get("data", [])
    return spaces