import json
import datetime as dt

from sqlalchemy import TypeDecorator, orm
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
    regions = db.Column(JsonColumn(255))
    work_hours = db.Column(JsonColumn(255))

    # if need to call some methods after the object is fetched from DB
    @orm.reconstructor
    def reconstruct(self):
        self.hours_list = []
        # if len(self.work_hours) <= 0:
        #     return
        for shift in self.work_hours:
            self.hours_list.append({
                'start': dt.time.fromisoformat(shift.split('-')[0]),
                'end': dt.time.fromisoformat(shift.split('-')[1])
            })

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
    dlvr_hours = db.Column(JsonColumn(255))

    @orm.reconstructor
    def reconstruct(self):
        self.hours_list = []
        for time in self.dlvr_hours:
            self.hours_list.append({
                'start': dt.time.fromisoformat(time.split('-')[0]),
                'end': dt.time.fromisoformat(time.split('-')[1])
            })

    def fits_in_time(self, courier: Courier) -> bool:
        """Determines if current order can be delivered by a provided courier
        this method checks Order's delivery hours and Courier's work hours.
        If Courier's hours list is empty, should return False (I suppose)
        """
        for shift in courier.hours_list:
            for delivery in self.hours_list:
                print(f'comparing: courier:{shift}       and order:{delivery}')
                latest_start = max(shift['start'], delivery['start'])
                eraliest_end = min(shift['end'], delivery['end'])
                print('latest_start', latest_start)
                print('earliest_end', eraliest_end)
                if latest_start <= eraliest_end:
                    return True
        return False

    def __repr__(self):
       return f'<Order {self.id} ({self.weight} kg) region:{self.region} hours:{self.dlvr_hours}>'

    # def __eq__(self, other):
    #     return (self.id == other.id and
    #             self.weight == other.weight and
    #             self.region == other.region and
    #             self.dlvr_hours == other.dlvr_hours)


class Assignment(db.Model):
    __tablename__ = 'assignments'

    c_id = db.Column(db.Integer, primary_key=True)
    o_id = db.Column(db.Integer, primary_key=True)
    o_region = db.Column(db.Integer)
    o_weight = db.Column(db.Float(precision=2))
    assign_time = db.Column(db.DateTime)
    complete_time = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Assignment (courier {self.c_id} -> order {self.o_id}) region {self.o_region} assigned: {self.assign_time} completed: {self.complete_time}>'
