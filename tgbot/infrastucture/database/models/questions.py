from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func, BIGINT

from tgbot.infrastucture.database.models.base import Base



class Question(Base):
    __tablename__ = 'questions'

    id = Column(BIGINT, primary_key=True)
    category = Column(VARCHAR(255), nullable=False)
    question = Column(VARCHAR(3000))
