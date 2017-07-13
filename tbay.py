import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Float,  String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


db_log_file = 'tbay.log'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_handler_log_level)


engine = create_engine('postgresql://ericsokolov:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    items = relationship("Item",  backref="users")
    bids = relationship("Bid", backref="users")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'),
                             nullable=False)

    bids = relationship("Bid", backref="items")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False)

    item_id = Column(Integer, ForeignKey('items.id'),
                     nullable=False)

Base.metadata.create_all(engine)

steve = User(username="Steve",password="badpassword")
frank = User(username="Frank",password="frankface")
tom = User(username="Tom",password="bingbong")

users = [steve,frank,tom]

basketball = Item(name="Basketball",description="A friggin' basketball", users=steve)
baseball = Item(name="Baseball",description="A friggin' baseball", users=tom)
football = Item(name="Football",description="A friggin' football", users=frank)

items = [basketball,baseball,football]

bid1 = Bid(price=5,users=tom,items=basketball)
bid2 = Bid(price=6,users=frank,items=basketball)
bid3 = Bid(price=7,users=tom,items=basketball)
bid4 = Bid(price=5,users=tom,items=football)

session.query(User.username, Item.name,Bid.price).join(Bid).join(Item).order_by(Bid.price.desc()).first()



session.add_all([steve,frank,tom,basketball,baseball,football,bid1,bid2,bid3,bid4])
session.commit()


for user in users:
    for item in user.items:
        print("{} is acutioning the item '{}'".format(user.username,item.name))

for user in users:
    for bid in user.bids:
        print("{} bid on the item {} for the price ${}".format(user.username,bid.items.name,bid.price))


for item in items:
    for bid in item.bids:
         print("The item {} has been bid on by {} for the price of {}".format(item.name,bid.users.username,bid.price))

print(session.query(User.username, Item.name,Bid.price).join(Bid).join(Item).order_by(Bid.price.desc()).first())
