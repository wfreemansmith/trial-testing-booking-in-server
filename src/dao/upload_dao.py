from src.logger import logger
from src.models import Upload, Candidate, Batch, FileUpload
from src.dao import BaseDAO
from src.utils import format_version_id
from typing import Dict
from sqlalchemy import select, func, and_
from datetime import datetime

# STEPS
# User uploads XLSX document
# BE Server reads this
# BE Server checks for missing fields, duplicate candidates, errors etc.
# BE Server returns JSON of XLSX info and a list of any errors
# FE Server renders this info in editable form
# User can edit info in-browser and add file uploads
# BE Server receives this, checks again for errors and duplicates
# If not ok, returns upldated JSON of XLSX info and a list of any errors
# If ok, BE Server inputs this information into the database


class UploadDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Candidate

    def get_next_part_delivery(self, marking_window_id: int, centre_id: str) -> str:
        """Returns next part delivery string based on count of previous uploads"""
        stmt = select(func.count()).where(
            and_(
                Upload.centre_id == centre_id,
                Upload.marking_window_id == marking_window_id
            )
        )

        count = self.session.execute(stmt).scalar_one()
        next_part = chr(count + 65)
        return next_part
    
    def create_upload_object(self, data: dict, marking_window_id: int, centre_id: int) -> Upload:
        """Recevies a dict and returns a Upload object nested with Candidate, Batch and File Upload objects"""
        version_id_reference = {}

        # format upload
        data['part_delivery'] = self.get_next_part_delivery(
            marking_window_id=marking_window_id,
            centre_id=centre_id
            )
        if not isinstance(data['test_date'], datetime):
            data['test_date'] = datetime.strptime(data['test_date'], "%Y-%m-%d") if data['test_date'] else None

        # create upload first
        data['marking_window_id'] = marking_window_id
        data['centre_id'] = centre_id
        upload_data = {k: v for k, v in data.items() if k not in ['batches', 'candidates']}
        upload = Upload(**upload_data)
        logger.debug(f"Creating upload '{upload.upload_id}'")

        # format batches, uploads and get batch_ids
        batches_data = data.pop('batches')
        batches = []
        for batch_data in batches_data:
            file_upload_data = batch_data.pop('file_uploads')
            batch_data.pop("errors", None)
            file_uploads = [FileUpload(**file_upload) for file_upload in file_upload_data]
            batch_data['upload_id'] = upload.upload_id
            batch = Batch(**batch_data, file_uploads=file_uploads)
            logger.debug(f"Creating batch '{batch.batch_id}'")
            version_id_reference[batch.version_id] = batch.batch_id
            batches.append(batch)

        # format candidates
        candidates_data = data.pop('candidates')
    
        candidates = []
        for candidate_data in candidates_data:
            candidate_data['upload_id'] = upload.upload_id
            for component in ('writing', 'reading', 'listening'):
                version_id = format_version_id(
                    paper=candidate_data.get("paper_sat"),
                    component=component,
                    version=candidate_data.pop(f'{component}_version'))
                candidate_data[f'{component}_batch_id'] = version_id_reference.get(version_id, None)
                candidate_data.pop(f'{component}_version_id', None)
                candidate_data.pop('errors', None)
            candidate = Candidate(**candidate_data)
            logger.debug(f"Creating candidate '{candidate.candidate_id}'")
            candidates.append(candidate)

        upload.batches = batches
        upload.candidates = candidates
        return upload

    def insert_upload(self, data: Dict, marking_window_id: int, centre_id: int):
        """Insert a single record into 'uploads' table from a provided data dict"""
        upload = self.create_upload_object(data, marking_window_id, centre_id)
        self.session.add(upload)
        self.session.commit()


