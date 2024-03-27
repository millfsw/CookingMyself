import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.id"))
    recipeid = Column(Integer, ForeignKey("recipes.id"))
    content = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now
    )
    status = sqlalchemy.Column(sqlalchemy.String)
    recipe = orm.relationship("Recipe")
    user = orm.relationship("User")
