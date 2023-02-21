from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func, BIGINT

from tgbot.infrastucture.database.models.base import Base



class Ideas(Base):
    __tablename__ = 'ideas'

    id = Column(BIGINT, primary_key=True)
    category = Column(VARCHAR(255))
    idea = Column(VARCHAR(3000))
    rate = Column(BIGINT)
