import pytest
from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.infrastucture.database.models.base import Base

class MockBot:
    def __init__(self):
        self.session = None

class MockMessage:
    def __init__(self, text="Test message", from_user=None, chat=None):
        self.text = text
        self.from_user = from_user or types.User(
            id=123456,
            is_bot=False,
            first_name="Test",
            username="test_user",
            language_code="ru"
        )
        self.chat = chat or types.Chat(id=123456, type="private")
        self.message_id = 1

class MockState:
    def __init__(self):
        self.storage = {}
        self.state = None

    async def get_state(self):
        return self.state

    async def set_state(self, state):
        self.state = state

    async def get_data(self):
        return self.storage

    async def update_data(self, **kwargs):
        self.storage.update(kwargs)

    async def set_data(self, data):
        self.storage = data

    async def finish(self):
        self.state = None
        self.storage = {}

@pytest.fixture(scope="session")
def config():
    return load_config(".env.test")

@pytest.fixture
async def engine(config):
    """Create test database engine"""
    engine = create_async_engine(
        config.db.construct_sqlalchemy_url('asyncpg'),
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(engine):
    """Create test database session"""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def message_mock():
    """Create mock message object"""
    return MockMessage()

@pytest.fixture
def state_mock():
    """Create mock state object"""
    return MockState()

@pytest.fixture
def bot_mock():
    """Create mock bot object"""
    return MockBot() 