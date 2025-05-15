from sqlalchemy.orm import sessionmaker

class BaseDAO():
    def __init__(self, engine):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close(self):
        self.session.close()