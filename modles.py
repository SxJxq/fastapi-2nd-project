from database import Base
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__="users"
    id=Column(Integer, nullable=False, primary_key=True)
    email=Column(String, nullable=False, unique=True)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    password=Column(String, nullable=False)