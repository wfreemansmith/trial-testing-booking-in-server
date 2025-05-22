from pydantic import BaseModel, Field
from typing import Optional, List


class ErrorMessage(BaseModel):
    field: str
    message: str = None

class CandidateDict(BaseModel):
    candidate_number: Optional[int]
    candidate_name: Optional[str]
    paper_sat: Optional[str]
    writing_version: Optional[str]
    reading_version: Optional[str]
    listening_version: Optional[str]
    writing_version_id: Optional[str]
    reading_version_id: Optional[str]
    listening_version_id: Optional[str]
    errors: List[ErrorMessage] = []

class BatchDict(BaseModel):
    version_id: str
    component_id: str
    errors: List[ErrorMessage] = []

class UploadPreviewData(BaseModel):
    centre_id: str = Field(pattern=r'^\d{4}$')
    marking_window_id: int

def validate_preview_data(data: dict) -> dict:
    return UploadPreviewData(**data).model_dump()

def parse_preview_data(data: dict) -> UploadPreviewData:
    return UploadPreviewData(**data)