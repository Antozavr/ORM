import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_table, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:USHxv246@localhost:5432/alchemy_db'

engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()
q = input('Введите имя издателя: ')
for qf in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale, Sale.count). \
        join(Publisher).join(Stock).join(Shop).join(Sale). \
        filter(Publisher.name == q):
    print(f'{qf.title} | {qf.name} | '
          f'{str(qf.price)} | {qf.date_sale}')


session.close()
