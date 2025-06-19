from src.dao import BaseDAO
from src.logger import logger
from src.models import MarkingWindow

class MarkingWindowDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session=session)
        self.model = MarkingWindow