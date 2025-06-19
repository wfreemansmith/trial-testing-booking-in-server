from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date


class ErrorMessage(BaseModel):
    field: str
    message: str = None

class CandidateDict(BaseModel):
    candidate_number: Optional[int] = 0
    candidate_name: Optional[str]
    paper_sat: Optional[str]
    writing_version: Optional[str]
    reading_version: Optional[str]
    listening_version: Optional[str]
    writing_version_id: Optional[str] = None
    reading_version_id: Optional[str] = None
    listening_version_id: Optional[str] = None
    errors: List[ErrorMessage] = []

    @field_validator("candidate_number", mode="before")
    def none_to_zero(cls, v):
        return 0 if v is None else v
    
def parse_candidate_data(data: dict) -> CandidateDict:
    return CandidateDict(**data)

class BatchDict(BaseModel):
    version_id: str
    component_id: str
    file_uploads: Optional[list] = []
    errors: List[ErrorMessage] = []

def parse_batch_data(data: dict) -> BatchDict:
    return BatchDict(**data)

class UploadPreviewData(BaseModel):
    centre_id: str = Field(pattern=r'^\d{4}$')
    marking_window_id: int

def validate_preview_data(data: dict) -> dict:
    return UploadPreviewData(**data).model_dump()

def parse_preview_data(data: dict) -> UploadPreviewData:
    return UploadPreviewData(**data)

class UploadFileData(BaseModel):
    centre_id: str = Field(pattern=r'^\d{4}$')
    marking_window_id: int
    batch: BatchDict
    candidates: List[CandidateDict]

def parse_uploadfile_data(data: dict) -> UploadFileData:
    return UploadFileData(**data)

class UploadData(BaseModel):
    centre_id: str = Field(pattern=r'^\d{4}$')
    marking_window_id: int
    epd_number: Optional[str] = None
    test_date: Optional[date] = None
    batches: List[BatchDict]
    candidates: List[CandidateDict]

def parse_upload_data(data: dict) -> UploadData:
    return UploadData(**data)

class UploadPayload(BaseModel):
    token: str
    data: dict