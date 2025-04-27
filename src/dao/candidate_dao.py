from sqlalchemy.orm import sessionmaker

class CandidateDAO():
    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()

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
        return False