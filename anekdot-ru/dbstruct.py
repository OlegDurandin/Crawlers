from peewee import *

db = SqliteDatabase('anekdot-ru.db')

class BaseModel(Model):
    class Meta:
        database = db

class Tags(BaseModel):
    url = TextField(unique=True)
    name = TextField()

class Authors(BaseModel):
    authorName = TextField()
    authorURL = TextField()

class Anecdot(BaseModel):
    anecdotID = IntegerField(unique=True, primary_key=True)
    text = TextField()
    positive = IntegerField(null=True)
    negative = IntegerField(null=True)
    url = TextField()
    authorID = ForeignKeyField(Authors, backref='authorID', null=True)
    date = DateField()

class TagsAnecdot(BaseModel):
    anecdotID = ForeignKeyField(Anecdot, backref='anectodID')
    tagID = ForeignKeyField(Tags, backref='tagID')

db.connect()
db.create_tables([Tags, Anecdot, TagsAnecdot,Authors])
