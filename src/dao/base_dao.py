from sqlalchemy import select, and_
from src.db import SessionLocal

class BaseDAO():
    def __init__(self, session):
        # if session is None:
        #     self.session = SessionLocal()
        #     self._owns_session = True
        self.session = session
        self.model = None

    def select(self, **kwargs):
        """Selects from model with key word arguments as AND conditions"""
        if not self.model:
            raise ValueError("Model is not set, please use the select function from child DAO and check that DAO sets the model.")
        
        if kwargs:
            conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
            stmt = select(self.model).where(and_(*conditions))
        else:
            stmt = select(self.model)

        return self.session.execute(stmt).scalars().all()
    
    def select_one(self, **kwargs):
        """Selects one entry from model with key word arguments"""
        if not self.model:
            raise ValueError("Model is not set, please use the select function from child DAO and check that DAO sets the model.")
        
        if kwargs:
            conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
            stmt = select(self.model).where(and_(*conditions))
        else:
            stmt = select(self.model)

        return self.session.execute(stmt).scalars().first()

    def close(self):
        self.session.close()