from src.dao import BaseDAO
from src.logger import logger
from src.models import StagedFile

class StagedFileDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = StagedFile

    def retrieve_file(self, centre_id, marking_window_id, version_id) -> StagedFile:
        """Uses key information to retrieve a file and returns temp path, filename and folder if present"""
        return self.select_one(centre_id=centre_id, marking_window_id=marking_window_id, version_id=version_id)        

    def stage_file(self, centre_id: str, marking_window_id: int, version_id: str, destination_filename: str, destination_folder: str, temp_path: str):
        """Adds file to staged table for upload or retrieval later"""
        staged_file = StagedFile(
            centre_id=centre_id,
            marking_window_id=marking_window_id,
            version_id=version_id,
            destination_folder=destination_folder,
            destination_filename=destination_filename,
            temp_path=temp_path)
        
        self.session.add(staged_file)
        self.session.commit()