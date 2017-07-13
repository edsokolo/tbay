import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

db_log_file = 'oneToMany.log'
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

class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    guitars = relationship("Guitar", backref = "manufacturer")

class Guitar(Base):
    __tablename__ = 'guitar'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'),
                             nullable = False)

Base.metadata.create_all(engine)

fender = Manufacturer(name="Fender")
strat = Guitar(name="Stratocaster", manufacturer=fender)
tele = Guitar(name="Telecaster")
fender.guitars.append(tele)

session.add_all([fender, strat, tele])
session.commit()

for guitar in fender.guitars:
    print(guitar.name)
print(tele.manufacturer.name)