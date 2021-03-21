import datetime as dt
from os import path
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config, settings


app = Flask(__name__)
app.config.from_object(Config)

slasty_db = SQLAlchemy(app)

# if not path.exists(f'{settings["basedir"]}/{settings["test_db"]}'):
#     slasty_db.create_all()

# courier type => max weight
courier_weights = {
    'foot': 10,
    'bike': 15,
    'car': 50
}

# from models import Courier, Order
import models

@app.shell_context_processor
def setup_shell_context():
    return {
        'db': slasty_db,
        'Courier': models.Courier,
        'Order': models.Order,
        'Assignment': models.Assignment,
        'c': models.Courier(
            id=123,
            c_type='foot',
            regions=[1, 12, 22],
            work_hours=['11:35-14:05', '09:00-11:00']
        ),
        'o': models.Order(
            id=456,
            weight=2.256,
            region=22,
            dlvr_hours=['09:00-12:00', '16:00-21:30']
        ),
        'a': models.Assignment(
            c_id=77,
            o_id=88,
            o_region=99,
            assign_time=dt.datetime.now(),
            complete_time=None,
            completed=False
        )
    }

@app.route('/', methods=['GET'])
def index():
    if not request.json:
        abort(400)
    for i in request.json:
        print(i == 'data')
        print(request.json['data'])
    return jsonify({'respone': 'OK'}), 200

@app.route('/couriers', methods=['POST'])
def upload_couriers():
    if not request.json or 'data' not in request.json:
        abort(400)
    couriers = []
    errors = []
    # absolutely horrible indentaion, but accepted by PEP8 validator
    for item in request.json['data']:
        # no necessary fields
        if ('courier_type' not in item or
                'regions' not in item or
                'working_hours' not in item):
                errors.append({'id': item['courier_id']})
                continue

        # extra fields
        if len(item) > 4:
            errors.append({'id': item['courier_id']})
            continue

        co = models.Courier(
            id=item['courier_id'],
            c_type=item['courier_type'],
            regions=item['regions'],
            work_hours=item['working_hours']
        )
        couriers.append(co)

    if len(errors) > 0:
        return jsonify({
            'validation_error': {
                'couriers': errors
            }
        }), 400

    slasty_db.session.add_all(couriers)
    slasty_db.session.commit()
    return jsonify({
        'couriers': list(map(lambda c: {'id': c.id}, couriers))
    }), 201

@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def update_couriers(courier_id):
    if not request.json:
        abort(400)
    patch = {}
    for item, val in request.json.items():
        if item == 'courier_type':
            patch[item] = val
        elif item == 'regions':
            patch[item] = val
        elif item == 'working_hours':
            patch[item] = val
        else:
            abort(400)

    result = slasty_db.session.query(models.Courier) \
        .filter(models.Courier.id == courier_id)

    if result.count() <= 0:
        abort(404)

    found_courier = result.first()
    for field, val in patch.items():
        if field == 'courier_type':
            found_courier.c_type = val
        elif field == 'regions':
            found_courier.regions = val
        elif field == 'working_hours':
            found_courier.work_hours = val

    slasty_db.session.commit()

    return jsonify(found_courier.as_dict()), 200

@app.route('/orders', methods=['POST'])
def upload_orders():
    if not request.json or 'data' not in request.json:
        abort(400)
    orders = []
    errors = []
    for item in request.json['data']:
        # no necessary fields
        if ('weight' not in item or
            'region' not in item or
            'delivery_hours' not in item):
            errors.append({'id': item['order_id']})
            continue

        # extra fields
        if len(item) > 4:
            errors.append({'id': item['order_id']})
            continue

        order = models.Order(
            id=item['order_id'],
            weight=item['weight'],
            region=item['region'],
            dlvr_hours=item['delivery_hours']
        )
        orders.append(order)

    if len(errors) > 0:
        return jsonify({
            'validation_error': {
                'orders': errors
            }
        }), 400

    slasty_db.session.add_all(orders)
    slasty_db.session.commit()
    return jsonify({
        'orders': list(map(lambda o: {'id': o.id}, orders))
    }), 201

@app.route('/orders/assign', methods=['POST'])
def assign_orders():
    if not request.json or 'courier_id' not in request.json:
        abort(400)
    courier_query = slasty_db.session.query(models.Courier) \
        .filter(models.Courier.id == request.json['courier_id'])
    if courier_query.count() <= 0:
        abort(400)

    # orders in courier's regions
    fetched_courier = courier_query.first()
    orders_query = slasty_db.session.query(models.Order) \
        .filter(models.Order.region.in_(fetched_courier.regions)) \
        .all()

    # orders which fit in courier's time
    orders = list(filter(lambda o: o.fits_in_time(fetched_courier), orders_query))
    if len(orders) <= 0:
        return jsonify({
            'orders': []
        }), 200

    # order by weight (asc)
    orders.sort(key=lambda o: o.weight)
    print(f'sorted orders in regions {fetched_courier.regions}:')
    for i in orders:
        print(i)

    weight_sum = 0
    avail_orders = []
    for order in orders:
        if (weight_sum + order.weight) <= courier_weights[fetched_courier.c_type]:
            print(f'take order: {order}')
            avail_orders.append(order)
            weight_sum += order.weight

    assign_time = dt.datetime.utcnow()
    for order in avail_orders:
        asg = models.Assignment(
            c_id=fetched_courier.id,
            o_id=order.id,
            o_region=order.region,
            assign_time=assign_time,
            complete_time=None,
            completed=False
        )
        slasty_db.session.add(asg)
    slasty_db.session.commit()
    return jsonify({
        'orders': list(map(lambda o: {'id': o.id}, avail_orders)),
        'assign_time': assign_time
    }), 200

@app.route('/orders/complete', methods=['POST'])
def complete_orders():
    pass

@app.route('/couriers/<int:courier_id>')
def rate_courier(courier_id):
    pass


if __name__ == '__main__':
    app.run(host=settings['host'], port=settings['port'], debug=settings['is_debug'])
