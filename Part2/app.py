from flask import Flask
from flask import jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config, settings

app = Flask(__name__)
app.config.from_object(Config)

slasty_db = SQLAlchemy(app)

@app.shell_context_processor
def setup_shell_context():
    from models import Courier, Order
    return {
        'db': slasty_db,
        'Courier': Courier,
        'c': Courier(
            id=123,
            c_type='foot',
            regions=[1, 12, 22],
            work_hours=['11:35-14:05', '09:00-11:00']
        ),
        'o': Order(
            id=456,
            weight=2.256,
            region=22,
            dlvr_hours=['09:00-12:00', '16:00-21:30']
        )
    }

@app.route('/', methods=['GET'])
def index():
    return jsonify({'respone': 'hello'})

@app.route('/couriers', methods=['POST'])
def upload_couriers():
    pass

@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def update_couriers(courier_id):
    pass

@app.route('/orders', methods=['POST'])
def upload_orders():
    pass

@app.route('/orders/assign', methods=['POST'])
def assign_orders():
    pass

@app.route('/orders/complete', methods=['POST'])
def complete_orders():
    pass

@app.route('/couriers/<int:courier_id>')
def rate_courier(courier_id):
    pass


if __name__ == '__main__':
    app.run(settings['host'], settings['port'], debug=settings['is_debug'])
