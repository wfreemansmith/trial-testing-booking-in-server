from src.logger import logger
from src.models import Upload, Candidate, Batch, FileUpload
from src.utils import format_version_id
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
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


class UploadDAO():
    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_next_part_delivery(self, session_id: int, centre_id: str) -> str:
        """Returns next part delivery string based on count of previous uploads"""
        stmt = select(func.count()).where(
            and_(
                Upload.centre_id == centre_id,
                Upload.session_id == session_id
            )
        )

        count = self.session.execute(stmt).scalar_one()
        next_part = chr(count + 65)
        return next_part
    
    def create_upload_object(self, data: Dict) -> Upload:
        """Recevies a dict and returns a Upload object nested with Candidate, Batch and File Upload objects"""
        version_batches = {}

        # format upload
        data['part_delivery'] = self.get_next_part_delivery(
            session_id=data.get('session_id'),
            centre_id=data.get('centre_id')
            )
        data['test_date'] = datetime.strptime(data['test_date'], "%Y-%m-%d") if data['test_date'] else None

        # format batches, uploads and get batch_ids
        batches_data = data.pop('batches')
        batches = []
        for batch_data in batches_data:
            file_upload_data = batch_data.pop('file_uploads')
            file_uploads = [FileUpload(**file_upload) for file_upload in file_upload_data]
            batch = Batch(**batch_data, file_uploads=file_uploads)
            version_batches[batch.version_id] = batch.batch_id
            batches.append(batch)

        # format candidates
        candidates_data = data.pop('candidates')
        candidates = []
        for candidate_data in candidates_data:
            for component in ('writing', 'reading', 'listening'):
                version_id = format_version_id(
                    paper=candidate_data.get("paper_sat"),
                    component=component,
                    version=candidate_data.pop(f'{component}_version'))
                candidate_data[f'{component}_batch_id'] = version_batches.get(version_id, None)
            candidate = Candidate(**candidate_data)
            candidates.append(candidate)

        return Upload(**data, candidates=candidates, batches=batches)


    def insert_upload(self, data: Dict):
        """Insert a single record into 'uploads' table from a provided data dict"""
        upload = self.create_upload_object(data)
        self.session.add(upload)
        self.session.commit()


