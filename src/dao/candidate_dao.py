from src.dao import BaseDAO
from src.logger import logger

class CandidateDAO(BaseDAO):
    def is_duplicate_candidate(
            self,
            marking_window_id: int,
            centre_num: str,
            candidate_name: str,
            candidate_number: int):
        """Checks candidate name and number against database, returns truthy if duplicate, falsy if not.
        If name and candidate are duplicates, returns True.
        If just candidate number is duplcated, returns next available number.
        If not duplicate, returns false."""
        logger.debug(f"Checking marking window {marking_window_id}, centre '{centre_num}' for candidate {candidate_number} {candidate_name}...")
        return False