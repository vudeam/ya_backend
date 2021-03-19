import json

from sqlalchemy import TypeDecorator
from sqlalchemy.orm import relationship
from app import slasty_db as db


class JsonColumn(TypeDecorator):
    """Allows to store JSON values as a table column
    """
    impl = db.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class Courier(db.Model):
    __tablename__ = 'couriers'

    id = db.Column(db.Integer, primary_key=True)
    c_type = db.Column(db.String(10))
    regions = db.Column(JsonColumn(128))
    work_hours = db.Column(JsonColumn(128))

    # if need to call some methods after the object is fetched from DB
    # @orm.reconstructor
    # def reconstruct(self):

    def as_dict(self):
        return {
        'courier_id': self.id,
        'courier_type': self.c_type,
        'regions': self.regions,
        'working_hours': self.work_hours
    }

    def __repr__(self):
        return f'<Courier {self.id} ({self.c_type}) regions:{self.regions} hours:{self.work_hours}>'


class Order(db.Model):
   __tablename__ = 'orders'

   id = db.Column(db.Integer, primary_key=True)
   weight = db.Column(db.Float(precision=2))
   region = db.Column(db.Integer)
   dlvr_hours = db.Column(JsonColumn(128))

   def __repr__(self):
       return f'<Order {self.id} ({self.weight}) region:{self.region} hours:{self.dlvr_hours}>'
