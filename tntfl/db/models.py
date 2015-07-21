from peewee import SqliteDatabase, Model, CharField, FloatField, ForeignKeyField,\
    IntegerField, DateTimeField


db = SqliteDatabase('ladder.db')


class BaseModel(Model):
    class Meta:
        database = db


class Player(BaseModel):
    name = CharField(unique=True)
    elo = FloatField(default=0)


class Game(BaseModel):
    redPlayer = ForeignKeyField(Player, related_name='gamesAsRed')
    bluePlayer = ForeignKeyField(Player, related_name='gamesAsBlue')
    redScore = IntegerField()
    blueScore = IntegerField()
    time = DateTimeField()
    deletedBy = CharField(null=True)
    deletedAt = DateTimeField(null=True)


class AchievementUnlock(BaseModel):
    player = ForeignKeyField(Player, related_name='achievements')
    game = ForeignKeyField(Game, related_name='achievements')
    type = CharField()

db.create_tables([Player, Game], safe=True)
