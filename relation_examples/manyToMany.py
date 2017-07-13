import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Float, String, DateTime, Date, ForeignKey
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

pizza_topping_table = Table('pizza_topping_association', Base.metadata,
                            Column('pizza_id', Integer, ForeignKey('pizza.id')),
                            Column('topping_id', Integer, ForeignKey('topping.id'))
                            )

class Pizza(Base):
    __tablename__ = 'pizza'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    toppings = relationship("Topping", secondary = "pizza_topping_association",
                            backref = "pizzas")

class Topping(Base):
    __tablename__ = 'topping'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

Base.metadata.create_all(engine)

peppers = Topping(name = "Peppers")
garlic = Topping(name = "Garlic")
chilli = Topping(name = "Chill")

spicy_pepper = Pizza(name="Spicy Pepper")
spicy_pepper.toppings = [peppers, chilli]

vampire_weekend = Pizza(name="Vampire Weekend")
vampire_weekend.toppings = [garlic, chilli]

session.add_all([garlic, peppers, chilli, spicy_pepper, vampire_weekend])
session.commit()

for topping in vampire_weekend.toppings:
    print(topping.name)

for pizza in chilli.pizzas:
    print(pizza.name)