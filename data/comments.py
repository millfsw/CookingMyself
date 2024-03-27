import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    recipeid = Column(Integer, ForeignKey("recipes.id"))
    content = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
