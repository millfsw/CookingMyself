import sqlalchemy
import datetime
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    recipeid = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("recipes.id")
    )
    content = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    changed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.String)
    recipe = relationship("Recipe")
    user = relationship("User")
