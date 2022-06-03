from peewee import *
import datetime


db = SqliteDatabase('telegram.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    balance = IntegerField(default=0)

    class Meta:
        db_table = 'users'


class Seed(BaseModel):
    seed = CharField(unique=True)
    balance = FloatField()

    class Meta:
        db_table = 'seeds'