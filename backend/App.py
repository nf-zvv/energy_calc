import math
import json
from flask import Flask, jsonify, make_response, abort, request, Response
from flask_cors import CORS
import sqlalchemy as db
#from sqlalchemy import create_engine, MetaData, select
#from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table

engine = db.create_engine('sqlite:///production.db', echo=False, connect_args={'timeout': 20})

connection = engine.connect()

metadata = db.MetaData()

machines_table = db.Table('machines', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('title', db.Text),
    db.Column('power', db.Integer)
)

products_table = db.Table('products', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('title', db.Text),
    db.Column('department', db.Integer),
    db.Column('operations', db.Text),
    db.Column('quantity', db.Text)
)

metadata.create_all(engine)

app = Flask(__name__)
CORS(app)


# Получение списка машин
@app.route('/energy/api/machines', methods=['GET'])
def get_machines():
    page = request.args.get('page', type = int)
    size = request.args.get('size', type = int)
    total_pages = None
    if page is not None and size is not None:
        with engine.begin() as conn:
            count = conn.execute(
                db.select(db.func.count("*")).select_from(machines_table)
            )
            count = count.fetchone()[0]
            total_pages = math.ceil(count/size)
            results = conn.execute(
                db.select(machines_table).limit(size).offset((page-1)*size)
            )
    else:
        with engine.begin() as conn:
            results = conn.execute(
                db.select(machines_table)
            )
    machines_list = results.fetchall()
    if not machines_list:
        abort(404)
    machines = [dict(zip(results.keys(),row)) for row in machines_list]
    if total_pages is not None:
        return jsonify({'data': machines, 'last_page': total_pages})
    else:
        return jsonify({'data': machines})
    

# Получение одной машины по ID
@app.route('/energy/api/machines/<int:machine_id>', methods=['GET'])
def get_machine(machine_id):
    with engine.begin() as conn:
        results = conn.execute(
            db.select(machines_table).where(machines_table.c.id == machine_id)
        )
        machines_list = results.fetchall()
        if not machines_list:
            abort(404)
        machine = [dict(zip(results.keys(),row)) for row in machines_list]
        return jsonify({'data': machine})


# Создание машины
@app.route('/energy/api/machines', methods=['POST'])
def create_machine():
    machine = request.get_json()
    with engine.begin() as conn:
        query = machines_table.insert().values(machine)
        result = conn.execute(query)
        return jsonify({'info':'Machine added'}), 201, {'Content-Type': 'application/json'}


# Обновление (редактирование) машины по ID
@app.route('/energy/api/machines/<int:machine_id>', methods=['PUT'])
def update_machine(machine_id):
    # Проверяем есть ли запись с таким ID
    with engine.connect() as conn:
        results = conn.execute(
            db.select(machines_table).where(machines_table.c.id == machine_id)
        )
        if not results.fetchall():
            abort(404)
    # Запись существует, значит можно обновлять
    machine = request.get_json()
    with engine.begin() as conn:
        query = machines_table.update().where(machines_table.c.id == machine_id).values({'title':machine['title'], 'power':machine['power']})
        result = conn.execute(query)
        return jsonify({'info':'Machine updated'}), 201, {'Content-Type': 'application/json'}


# Удаление машины по ID
@app.route('/energy/api/machines/<int:machine_id>', methods=['DELETE'])
def delete_machine(machine_id):
    # Проверяем есть ли запись с таким ID
    with engine.connect() as conn:
        results = conn.execute(
            db.select(machines_table).where(machines_table.c.id == machine_id)
        )
        if not results.fetchall():
            abort(404)
    # Запись существует, значит удаляем
    with engine.begin() as conn:
        conn.execute(
            db.delete(machines_table).where(machines_table.c.id == machine_id)
        )
        return jsonify({'info':'Machine deleted'}), 200, {'Content-Type': 'application/json'}


# Получение списка продукции
@app.route('/energy/api/products', methods=['GET'])
def get_products():
    page = request.args.get('page', type = int)
    size = request.args.get('size', type = int)
    department = request.args.get('dep', type = int)
    total_pages = None
    if department is not None and page is not None and size is not None:
        with engine.begin() as conn:
            count = conn.execute(
                db.select(db.func.count("*")).select_from(products_table)
            )
            count = count.fetchone()[0]
            total_pages = math.ceil(count/size)
            results = conn.execute(
                db.select(products_table).where(products_table.c.department == department).limit(size).offset((page-1)*size)
            )
    elif page is not None and size is not None:
        with engine.begin() as conn:
            count = conn.execute(
                db.select(db.func.count("*")).select_from(products_table)
            )
            count = count.fetchone()[0]
            total_pages = math.ceil(count/size)
            results = conn.execute(
                db.select(products_table).limit(size).offset((page-1)*size)
            )
    elif department is not None:
        with engine.begin() as conn:
            results = conn.execute(
                db.select(products_table).where(products_table.c.department == department)
            )
    else:
        with engine.begin() as conn:
            results = conn.execute(
                db.select(products_table)
            )
    products_list = results.fetchall()
    if not products_list:
        abort(404)
    products = [dict(zip(results.keys(),row)) for row in products_list]
    for product in products:
        operations = product['operations']
        product['operations'] = json.loads(operations)
    if total_pages is not None:
        return jsonify({'data': products, 'last_page': total_pages})
    else:
        return jsonify({'data': products})


# Получение одного продукта по ID
@app.route('/energy/api/products/<int:product_id>', methods=['GET'])
def get_product_id(product_id):
    with engine.begin() as conn:
        results = conn.execute(
            db.select(products_table).where(products_table.c.id == product_id)
        )
        products_list = results.fetchall()
    if not products_list:
        abort(404)
    products = [dict(zip(results.keys(),row)) for row in products_list]
    for product in products:
        operations = product['operations']
        product['operations'] = json.loads(operations)
    return jsonify({'data': products})


# Создание продукта
@app.route('/energy/api/products', methods=['POST'])
def create_product():
    product = request.get_json()
    with engine.begin() as conn:
        query = products_table.insert().values({'title':product['title'], 'operations':json.dumps(product['operations']), 'quantity':product['quantity'], 'department':product['department']})
        result = conn.execute(query)
        return jsonify({'info':'Product added'}), 201, {'Content-Type': 'application/json'}


# Обновление (редактирование) продукта по ID
@app.route('/energy/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Проверяем есть ли запись с таким ID
    with engine.connect() as conn:
        results = conn.execute(
            db.select(products_table).where(products_table.c.id == product_id)
        )
        if not results.fetchall():
            abort(404)
    # Запись существует, значит можно обновлять
    product = request.get_json()
    with engine.begin() as conn:
        query = products_table.update().where(products_table.c.id == product_id).values({'title':product['title'], 'operations':json.dumps(product['operations']), 'quantity':product['quantity'], 'department':product['department']})
        result = conn.execute(query)
        return jsonify({'info':'Product updated'}), 201, {'Content-Type': 'application/json'}


# Удаление продукта по ID
@app.route('/energy/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Проверяем есть ли запись с таким ID
    with engine.connect() as conn:
        results = conn.execute(
            db.select(products_table).where(products_table.c.id == product_id)
        )
        if not results.fetchall():
            abort(404)
    # Запись существует, значит удаляем
    with engine.begin() as conn:
        conn.execute(
            db.delete(products_table).where(products_table.c.id == product_id)
        )
        return jsonify({'info':'Product deleted'}), 200, {'Content-Type': 'application/json'}


# Расчет потребления энергии цехом/предприятием
@app.route('/energy/api/consumption', methods=['GET'])
def get_consumption():
    department = request.args.get('dep', type = int)
    total_pages = None
    if department is not None:
        with engine.begin() as conn:
            results = conn.execute(
                db.select(products_table).where(products_table.c.department == department)
            )
    else:
        with engine.begin() as conn:
            results = conn.execute(
                db.select(products_table)
            )
    products_list = results.fetchall()
    if not products_list:
        abort(404)
    products = [dict(zip(results.keys(),row)) for row in products_list]
    for product in products:
        operations = product['operations']
        product['operations'] = json.loads(operations)
    
    # Расчет энергопотребления
    power_consumption = []
    for product in products:
        item = {}
        item['id'] = product['id']
        item['title'] = product['title']
        energy = 0
        for operation in product['operations']:
            machine_id = operation['machine']
            machine_power = get_machine_power(machine_id)
            energy += machine_power * float(operation['power_factor']) * float(operation['duration'])
        item['energy'] = energy
        item['energy_full'] = energy * float(product['quantity'])
        power_consumption.append(item)
    return jsonify({'data': power_consumption})


def get_machine_power(machine_id):
    with engine.begin() as conn:
        results = conn.execute(
            db.select(machines_table.c.power).where(machines_table.c.id == machine_id)
        )
    machine_power = results.fetchone()[0]
    return machine_power



@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res


# Обработчик ошибки 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Обработчик ошибки 405
@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


if __name__ == '__main__':
    app.run(debug=True)
