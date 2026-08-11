from fastapi import APIRouter

router = APIRouter( prefix="/health", tags=["Health"], )

@router.get("") 
async def health_check() -> dict[str, str]: 
    """ Return the current 
    application health status. """ 

    return { "status": "healthy", }