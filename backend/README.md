# Серверная часть программы расчета потребления энергии

Серверная часть (backend) программы расчета потребления энергии.

Серверная часть разработана на Python, обработкой запросов занимается Flask, в качестве базы данных используется SQLite через библиотеку SQLAlchemy.

## Установка на новом месте

Склонировать репозиторий (или скачать архив с гитхаба).

Перейти в директорию с проектом и создать виртуальное окружение:

```
python -m venv env
```

Активировать виртуальное окружение:

```
env\Scripts\activate
```

Установить требуемые пакеты:

```
pip install -r requirements.txt
```

Заполнить базу данных тестовыми записями:

```
python fill_db.py
```

## Запуск сервера

Перейти в директорию с проектом.

Активировать виртуальное окружение:

```
env\Scripts\activate
```

Запустить сервер:

```
python App.py
```

## Проверка работы серверной части с помощью Curl

### Работа с машинами

Получение всех машин (GET-запрос):

```
curl -i http://127.0.0.1:5000/energy/api/machines
```

Получение 5-й машины (GET-запрос):

```
curl -i http://127.0.0.1:5000/energy/api/machines/5
```

Добавление машины (POST-запрос):

```
curl -i -H "Content-Type: application/json" -d "{\"title\": \"Hell machine\", \"power\": 666}" http://127.0.0.1:5000/energy/api/machines
```

Обновление машины (PUT-запрос):

```
curl -i -X PUT -H "Content-Type: application/json" -d "{\"id\": 5, \"title\": \"Good machine\", \"power\": 777}" http://127.0.0.1:5000/energy/api/machines/5
```

Удаление 5-й машины (DELETE-запрос):

```
curl -i -X DELETE http://127.0.0.1:5000/energy/api/machines/5
```

### Работа с продукцией

Получение всей продукции (GET-запрос):

```
curl -i http://127.0.0.1:5000/energy/api/products
```

Получение 2-го продукта (GET-запрос):

```
curl -i http://127.0.0.1:5000/energy/api/products/2
```

Добавление продукта (POST-запрос):

не работает:

```
curl -i -H "Content-Type: application/json" -d "{\"title\": \"Hellstone\", \"quantity\": 6, \"department\":1, \"operations\": \"\"[{\"machine\": 3, \"power_factor\": 0.65, \"duration\": 30},{\"machine\": 1, \"power_factor\": 0.7, \"duration\": 25}]\"\"}" http://127.0.0.1:5000/energy/api/products
```

```
curl -i -H "Content-Type: application/json" -d "{\"title\": \"Hellstone\", \"quantity\": 6, \"department\":1, \"operations\": \"operations list...\"}" http://127.0.0.1:5000/energy/api/products
```

Обновление продукта (PUT-запрос):


```
curl -i -X PUT -H "Content-Type: application/json" -d "{\"title\": \"Hell sword\", \"quantity\": 4, \"department\":1, \"operations\": \"new operations list...\"}" http://127.0.0.1:5000/energy/api/products/1
```

Удаление 2-го продукта (DELETE-запрос):

```
curl -i -X DELETE http://127.0.0.1:5000/energy/api/products/2
```



## API

Обмен сообщениями между клиентской частью (frontend) и серверной (backend) ведется в формате JSON.

Flask REST API

API URL:

```
http://127.0.0.1:5000/energy/api/<action>
```

### Машины

| Действие   | HTTP метод |          URL           |           Описание             |
|------------|------------|------------------------|--------------------------------|
| Чтение     | GET        | /machines              | Получение списка всех машин    |
| Чтение     | GET        | /machines/<machine_ID> | Получение одной машины         |
| Создание   | POST       | /machines              | Создание новой машины          |
| Обновление | PUT        | /machines/<machine_ID> | Обновление существующей машины |
| Удаление   | DELETE     | /machines/<machine_ID> | Удаление существующей машины   |

### Продукция

| Действие   | HTTP метод |          URL           |           Описание                |
|------------|------------|------------------------|-----------------------------------|
| Чтение     | GET        | /products              | Получение списка всех продуктов   |
| Чтение     | GET        | /products?dep=<dep_ID> | Получение списка продуктов цеха   |
| Чтение     | GET        | /products/<product_ID> | Получение одного продукта         |
| Создание   | POST       | /products              | Создание нового продукта          |
| Обновление | PUT        | /products/<product_ID> | Обновление существующего продукта |
| Удаление   | DELETE     | /products/<product_ID> | Удаление существующего продукта   |

### Получение списка всех машин

Запрос, метод GET:

```
http://127.0.0.1:5000/energy/api/machines
```

Ответ:

```json
{
  "data": [
    {
      "id": 1,
      "power": 3000,
      "title": "Станок токарный"
    },
    {
      "id": 2,
      "power": 1050,
      "title": "Станок сверлильный"
    },
    {
      "id": 3,
      "power": 2500,
      "title": "Станок токарный"
    }
  ]
}
```

### Получение данных о машине по ID

Запрос, метод GET:

```
http://127.0.0.1:5000/energy/api/machines/<machine_ID>
```

Ответ:

```json
{
  "data": [
    {
      "id": 1,
      "power": 3000,
      "title": "Станок токарный"
    }
  ]
}
```

### Добавление машины


Запрос, метод POST:

```
http://127.0.0.1:5000/energy/api/machines
```

Содержимое POST-сообщения:

```json
{
    "power": 3000,
    "title": "Станок токарный"
}
```

При успешном создании возвращается код 201 и сообщение:

```json
{info: 'Machine added'}
```

### Редактирование машины

Запрос, метод PUT:

```
http://127.0.0.1:5000/energy/api/machines
```

Содержимое POST-сообщения:

```json
{
    "power": 3000,
    "title": "Станок токарный"
}
```

При успешном обновлении возвращается код 201 и сообщение:

```json
{info: 'Machine updated'}
```

### Удаление машины

Запрос, метод DELETE:

```
http://127.0.0.1:5000/energy/api/machines/<machine_ID>
```

При успешном удалении возвращается код 200 и сообщение:

```json
{info: 'Machine deleted'}
```

