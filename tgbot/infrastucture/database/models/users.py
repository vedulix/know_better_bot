from sqlalchemy import Column, BIGINT, VARCHAR, TIMESTAMP, ForeignKey, Integer, BOOLEAN, Boolean
from sqlalchemy.sql import func

from tgbot.infrastucture.database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(BIGINT, primary_key=True)
    username = Column(VARCHAR(255))
    full_name = Column(VARCHAR(255), nullable=False)
    language_code = Column(VARCHAR(10), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_activity = Column(TIMESTAMP)

    active = Column(Boolean, unique=False, default=True)
    reflection_time = Column(Integer, server_default='19')

    referrer_id = Column(BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL'))
    deep_link = Column(VARCHAR(255), server_default=None)
