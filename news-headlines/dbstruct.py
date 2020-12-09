from peewee import *

db = SqliteDatabase('ru-newsheadlines.db')


class BaseModel(Model):
    class Meta:
        database = db

class LentaHeads(BaseModel):
    date = DateField()
    time = TimeField()
    url = TextField(unique=True)
    header = TextField()

class LentaNews(BaseModel):
    newsId = ForeignKeyField(LentaHeads, backref='headID', null=True)
    head = TextField()
    text = TextField()


db.connect()
db.create_tables([LentaHeads, LentaNews])
