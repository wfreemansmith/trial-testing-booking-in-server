from sqlalchemy import select, and_
from src.db import SessionLocal

class BaseDAO():
    def __init__(self, session=None):
        if session is None:
            self.session = SessionLocal()
            self._owns_session = True
        else:
            self.session = session
            self._owns_session = False
        self.model = None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._owns_session:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()

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
        """Explicitly close session if owned by DAO"""
        if self._owns_session and self.session:
            self.session.close()

    def commit(self):
        """Commit the current transaction"""
        if self.session:
            self.session.commit()

    def rollback(self):
        if self.session:
            self.session.rollback()