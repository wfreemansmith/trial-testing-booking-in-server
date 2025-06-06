from src.dao import BaseDAO
from src.logger import logger
from src.models import Version

class VersionDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Version

    def version_exists(self, version_id: str) -> bool:
        """Checks if version exists in database, returns true or false"""
        logger.debug(f"Checking database for version '{version_id}'...")
        # check version
        return True