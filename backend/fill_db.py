import sqlalchemy as db
import json


engine = db.create_engine('sqlite:///production.db', echo=True, connect_args={'timeout': 20})

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

machines_query = machines_table.insert().values([
    {'title':'Станок токарный', 'power':3000},
    {'title':'Станок сверлильный', 'power':1050},
    {'title':'Станок токарный', 'power':2500},
    {'title':'Станок фрезерный', 'power':3100}
])


operations_1 = [
            {
                'machine': 1, 
                'power_factor': 0.70, 
                'duration': 50
            },
            {
                'machine': 4,
                'power_factor': 0.65,
                'duration': 35
            }
        ]
operations_1 = json.dumps(operations_1)


operations_2 = [
            {
                'machine': 3,
                'power_factor': 0.65,
                'duration': 30
            },
            {
                'machine': 2,
                'power_factor': 0.65,
                'duration': 10
            },
            {
                'machine': 4,
                'power_factor': 0.65,
                'duration': 60
            }
        ]
operations_2 = json.dumps(operations_2)

products_query = products_table.insert().values([
    {
        'title': 'Вал ступенчатый стальной', 
        'department': 1, 
        'quantity': 10, 
        'operations': operations_1
    },
    {
        'title': 'Шестерня стальная',
        'department': 1, 
        'quantity': 10,
        'operations': operations_2
    },
])

# Добавляем машины
with engine.begin() as conn:
    result = conn.execute(machines_query)
    print(result.all)

# Добавляем продукцию
with engine.begin() as conn:
    result = conn.execute(products_query)
    print(result.all)


# Выводим список машин
with engine.begin() as conn:
    results = conn.execute(
        db.select(machines_table)
    )
    machines = [dict(zip(results.keys(),row)) for row in results.fetchall()]
    print(machines)

