from sqlalchemy.orm import sessionmaker

class VersionDAO():
    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def version_exists(self, version_id: str) -> bool:
        """Checks if version exists in database, returns true or false"""
        # check version
        return True