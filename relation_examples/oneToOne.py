import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float,  String, DateTime, Date, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

db_log_file = 'oneToOne.log'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_handler_log_level)


engine = create_engine('postgresql://ericsokolov:thinkful@localhost:5432/ericsokolov')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    passport = relationship("Passport", uselist=False, backref="owner")

class Passport(Base):
    __tablename__ = 'passport'
    id = Column(Integer, primary_key=True)
    issue_date = Column(Date, nullable=False, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('person.id'), nullable=False)

Base.metadata.create_all(engine)

beyonce = Person(name="Beyonce Knowles")
steve = Person(name="Steve Butt")
passport = Passport()
passport1 = Passport()
beyonce.passport = passport
steve.passport = passport1

session.add(beyonce)
session.add(steve)
session.commit()

print(beyonce.passport.issue_date)
print(passport.owner.name)
print(steve.passport.issue_date)
print(passport1.owner.name)