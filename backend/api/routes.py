from fastapi import APIRouter, HTTPException

from backend.models.schemas import (
    VerifyRequest,
    VerificationResponse
)

from backend.services.pipeline import verify_content


router = APIRouter(
    prefix="/api/v1",
    tags=["Verification"]
)


@router.post(
    "/verify",
    response_model=VerificationResponse
)
def verify(request: VerifyRequest):

    if not request.text and not request.url:

        raise HTTPException(
            status_code=400,
            detail="Provide either text or URL."
        )

    try:

        result = verify_content(
            text=request.text,
            url=request.url
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )