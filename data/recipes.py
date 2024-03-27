import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase):
    __tablename__ = "recipes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    status = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relationship("User")
