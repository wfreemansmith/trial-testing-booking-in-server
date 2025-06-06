from sqlalchemy import select, and_
from sqlalchemy.orm import sessionmaker

class BaseDAO():
    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model = None

    def select(self, **kwargs):
        if not self.model:
            raise ValueError("Model is not set, please use the select function from child DAO and check that DAO sets the model.")
        
        if kwargs:
            conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
            stmt = select(self.model).where(and_(*conditions))
        else:
            stmt = select(self.model)

        return self.session.execute(stmt).scalars().all()

    def close(self):
        self.session.close()