from src.dao import BaseDAO
from src.logger import logger
from src.models import Centre

class CentreDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = Centre