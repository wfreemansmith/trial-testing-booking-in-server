from sqlalchemy import select, and_
from src.dao import BaseDAO
from src.logger import logger
from src.models import Candidate

class CandidateDAO(BaseDAO):
    def __init__(self, engine):
        super().__init__(engine=engine)
        self.model = Candidate
        
    def get_candidates(self, **kwargs):
        """Get candidates by keyword arguments"""
        if len(kwargs) > 1:
            stmt = select(Candidate).where(
                and_(
                    getattr(Candidate, k) == v for k, v in kwargs.items()
                )
            )

    def is_duplicate_candidate(
            self,
            marking_window_id: int,
            centre_num: str,
            candidates: list
            ):
        """Checks candidate names and numbers against database, returns truthy if duplicate, falsy if not.
        If name and candidate are duplicates, returns True.
        If just candidate number is duplcated, returns next available number.
        If not duplicate, returns false.
        Accepts list of number, name, or a list of lists"""
        if isinstance(candidates[0], int) and isinstance(candidates[1], str):
            candidate_list = [candidates]
        elif isinstance(candidates[0], list):
            candidate_list = candidates
        else:
            raise Exception("Wrong candidate type provided to 'is_duplicate_candidate'")
        
        # logger.debug(f"Checking marking window {marking_window_id}, centre '{centre_num}' for duplicate candidates...")
        # # get uploads from centre on db
        # existing_uploads = []
        
        # duplicates_found = 0
        # list_to_return = []
        # for candidate in candidate_list:
        #     if candidate[0] in existing_uploads[0] and candidate[1] in existing_uploads[1]:
        #         list_to_return.append(True)
            
        return False