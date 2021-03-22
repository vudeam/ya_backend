import datetime as dt
from dateutil import parser
from os import path
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from config import Config, settings

# TODO: unassign extra orders on courier's PATCH
# TODO: add errors descriptions

app = Flask(__name__)
app.config.from_object(Config)

slasty_db = SQLAlchemy(app)

# courier type => max weight
courier_weights = {
    'foot': 10.0,
    'bike': 15.0,
    'car': 50.0
}

import models

@app.shell_context_processor
def setup_shell_context():
    """Used to have some values defined when you call `flask shell`
    in the project folder. Good for testing things out
    """
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
            o_weight=1.23,
            assign_time=dt.datetime.now(),
            complete_time=None,
            completed=False
        )
    }

@app.route('/', methods=['GET'])
def index():
    if not request.json:
        abort(400)
    for i, val in request.json.items():
        print(val)
        print(type(val))
        try:
            t = dt.datetime.fromisoformat(val)
            print(t)
        except ValueError:
            pass
    return jsonify({'respone': 'OK'}), 200

@app.route('/couriers', methods=['POST'])
def upload_couriers():
    if not request.json or 'data' not in request.json:
        abort(400)

    all_ids = [ c_id for c_id, in
        slasty_db.session.query(models.Courier.id).all()
    ]
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

        # courier id is taken
        if item['courier_id'] in all_ids:
            errors.append({'id': item['courier_id']})
            continue

        # wrong courier type
        if item['courier_type'] not in ['foot', 'bike', 'car']:
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

        if item['weight'] < .01 or item['weight'] > 50:
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

    # orders not taken by others and not completed
    not_avail_orders = [ o_id for o_id, in
        slasty_db.session.query(models.Assignment.o_id) \
            .all()
    ]
    # .filter(models.Assignment.c_id == fetched_courier.id) \
    # .filter(models.Assignment.completed == True) \

    # convert assignments to list of ids
    # not_avail_ids = list(map(lambda a: a.o_id, not_avail_orders))

    # orders which fit in courier's time
    orders = list(filter(lambda o: o.fits_in_time(fetched_courier), orders_query))
    # if len(orders) <= 0:
    #     return jsonify({
    #         'orders': []
    #     }), 200

    # order by weight (asc)
    orders.sort(key=lambda o: o.weight)

    # courier's load is sum(seights) of assigned (and not completed) orders
    load = slasty_db.session.query(func.sum(models.Assignment.o_weight)) \
        .filter(models.Assignment.c_id == fetched_courier.id) \
        .filter(models.Assignment.completed == False) \
        .scalar()
    if load is None:
        load = 0
    load = round(load, 2)
    print(f'courier has {load} kg')

    weight_sum = 0 + load
    avail_orders = []
    for order in orders:
        # skip unavailable order
        if order.id in not_avail_orders:
            continue
        if (weight_sum + order.weight) <= courier_weights[fetched_courier.c_type]:
            print(f'take order: {order}')
            avail_orders.append(order)
            weight_sum += order.weight
            print(f'now loaded with {weight_sum}')

    if len(avail_orders) <= 0:
        return jsonify({
            'orders': []
        }), 200

    assign_time = dt.datetime.utcnow()
    for order in avail_orders:
        asg = models.Assignment(
            c_id=fetched_courier.id,
            o_id=order.id,
            o_region=order.region,
            o_weight=order.weight,
            assign_time=assign_time,
            complete_time=None,
            completed=False
        )
        slasty_db.session.add(asg)
    slasty_db.session.commit()
    return jsonify({
        'orders': list(map(lambda o: {'id': o.id}, avail_orders)),
        'assign_time': assign_time.isoformat(timespec='milliseconds') + 'Z'
    }), 200

@app.route('/orders/complete', methods=['POST'])
def complete_orders():
    if not request.json:
        abort(400)
    if ('courier_id' not in request.json or
            'order_id' not in request.json or
            'complete_time' not in request.json):
            abort(400)

    try:
        details = {
            'c_id': request.json['courier_id'],
            'o_id': request.json['order_id'],
            # 'time': dt.datetime.fromisoformat(request.json['complete_time'])
            'time': parser.parse(request.json['complete_time'])
        }
    except:
        abort(400)

    assignment_query = slasty_db.session.query(models.Assignment) \
        .filter(models.Assignment.c_id == details['c_id']) \
        .filter(models.Assignment.o_id == details['o_id'])
    if assignment_query.count() <= 0:
        abort(400)

    # complete order
    assignment_query.first().completed = True
    assignment_query.first().complete_time = details['time']
    slasty_db.session.commit()
    return jsonify({
        'order_id': details['o_id']
    })

@app.route('/couriers/<int:courier_id>', methods=['GET'])
def rate_courier(courier_id):
    result = slasty_db.session.query(models.Courier) \
        .filter(models.Courier.id == courier_id)

    if result.count() <= 0:
        abort(404)

    fetched_courier = result.first()
    courier_dict = fetched_courier.as_dict()
    courier_dict['rating'] = ''
    courier_dict['earnings'] = ''
    return jsonify(courier_dict), 200


if __name__ == '__main__':
    app.run(host=settings['host'], port=settings['port'], debug=settings['is_debug'])
