from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func, BIGINT, ForeignKey

from tgbot.infrastucture.database.models.base import Base



class Answers(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BIGINT, ForeignKey('users.telegram_id', ondelete=None), nullable=False)
    #question_id = Column(BIGINT, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    question_id = Column(BIGINT, nullable=False)
    category = Column(VARCHAR(255), nullable=False)
    answer = Column(VARCHAR(3000))
    created_at = Column(TIMESTAMP, server_default=func.now())

