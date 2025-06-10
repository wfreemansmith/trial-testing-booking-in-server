from sqlalchemy import select
from src.dao import BaseDAO
from src.logger import logger
from src.models import Candidate, Upload
from itertools import chain

class CandidateDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Candidate

    def select_candidates_by_upload(self, marking_window_id: int, centre_id: str):
        """Finds candidates by upload id markers"""
        stmt = select(self.model).where(self.model.candidate_id.like(f'{marking_window_id}_{centre_id}%'))
        return self.session.execute(stmt).scalars().all()

    def is_duplicate_candidate(
            self,
            marking_window_id: int,
            centre_id: str,
            candidates: list
            ):
        """Checks candidate names and numbers against database, returns truthy if duplicate, falsy if not.
        If name and candidate are duplicates, returns True.
        If just candidate number is duplcated, returns next available number.
        If not duplicate, returns false.
        Accepts list of number, name, or a list of lists"""
        
        # prepares input
        if isinstance(candidates[0], int) and isinstance(candidates[1], str):
            candidate_list = [candidates]
        elif isinstance(candidates[0], list):
            candidate_list = candidates
        else:
            raise Exception("Wrong candidate type provided to 'is_duplicate_candidate'")
        
        logger.debug(f"Checking {len(candidate_list)} candidates for duplicates in marking window {marking_window_id}, centre '{centre_id}'...")
        
        # get existing candidates from database
        existing_candidates = self.select_candidates_by_upload(marking_window_id, centre_id)
        if not existing_candidates:
            return [False] * len(candidate_list)

        # finds the highest existing cand number in either the provided list or the db
        last_cand_num = max(
            chain(
                (candidate.candidate_number for candidate in existing_candidates),
                (candidate[0] for candidate in candidate_list)
                )
        )

        # for each candidate, finds whether they are duplicates or not and returns as a list
        list_to_return = []

        for candidate in candidate_list:
            if any(entry.candidate_number == candidate[0] and entry.candidate_name == candidate[1] for entry in existing_candidates):
                # returns True if same candidate name & number are found in db
                list_to_return.append(True)
            elif any(entry.candidate_number == candidate[0] and entry.candidate_name != candidate[1] for entry in existing_candidates):
                # returns a new number if just the candidate number is duplicated
                last_cand_num += 1
                list_to_return.append(last_cand_num)
            else:
                # returns false if not a duplicate
                list_to_return.append(False)
            
        return list_to_return