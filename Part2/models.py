import json

from sqlalchemy import Column, Float, String, Integer, TypeDecorator
from sqlalchemy.orm import relationship
from app import slasty_db as db


class JsonColumn(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class Courier(db.Model):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True)
    c_type = Column(String(10))
    regions = Column(JsonColumn(128))
    work_hours = Column(JsonColumn(128))

    def __repr__(self):
        return f'<Courier {self.id} ({self.c_type}) regions:{self.regions} hours:{self.work_hours}>'


class Order(db.Model):
   __tablename__ = 'orders'

   id = Column(Integer, primary_key=True)
   weight = Column(Float(precision=2))
   region = Column(Integer)
   dlvr_hours = Column(JsonColumn(128))

   def __repr__(self):
       return f'<Order {self.id} ({self.weight}) region:{self.region} hours:{self.dlvr_hours}>'
