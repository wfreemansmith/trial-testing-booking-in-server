from typing import List, Dict
from logger import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, and_
from src.models import Upload, Candidate
from datetime import datetime


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

    def format_upload_json(self, data: Dict):
        """Formats dict for upload for upload"""
        # format upload data
        data['centre_id'] = str(data['centre_id'])
        data['part_delivery'] = self.get_next_part_delivery(data['session_id'], data['centre_id'])
        data['test_date'] = datetime.strptime(data['test_date'], "%Y-%m-%d") if data['test_date'] else None

        # format candidates
        candidates_data = data.pop('candidates')
        candidates = [Candidate(**candidate) for candidate in candidates_data]

        for candidate in candidates:
            paper = candidate['paper_sat']
            writing = candidate.pop('writing_version')
            candidate['writing_version_id'] = f"{paper}W{writing}"
            reading = candidate.pop('reading_version')
            candidate['writing_version_id'] = f"{paper}R{reading}"
            listening = candidate.pop('listening_version')
            candidate['writing_version_id'] = f"L{listening}"
        
        return Upload(**data, candidates=candidates)


    def insert_many(self, data: Upload):
        """Insert records into Upload table from a list of JSON data"""
        candidates = data.pop('candidates')

        data = [Upload(**item) for item in data]
        self.session.add_all(data)