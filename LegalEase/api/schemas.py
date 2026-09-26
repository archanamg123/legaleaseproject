from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=3000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    jurisdiction: str = Field(
        default="",
        max_length=300
    )

    language: str = Field(
        default="English",
        max_length=50
    )


class DocumentResponse(BaseModel):
    success: bool
    document: str
    message: str = ""