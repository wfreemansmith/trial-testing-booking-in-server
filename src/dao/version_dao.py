from src.dao import BaseDAO
from src.logger import logger

class VersionDAO(BaseDAO):
    def version_exists(self, version_id: str) -> bool:
        """Checks if version exists in database, returns true or false"""
        logger.debug(f"Checking database for version '{version_id}'...")
        # check version
        return True