from fastapi import APIRouter, HTTPException

from api.schemas import (
    DocumentRequest,
    DocumentResponse,
)

from ai_core.gemini_generator import (
    GeminiDocumentGenerator,
)


router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(request: DocumentRequest):

    try:
        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            language=request.language,
        )

        return DocumentResponse(
            success=True,
            document=document,
            message="Document generated successfully.",
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )