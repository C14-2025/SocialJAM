"""
Configurações e fixtures para testes do backend SocialJAM
"""
import pytest
import pytest_asyncio
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import base, get_db
from app.core.mongo import get_mongo_db_with_check
from main import app

# Configurar variável de ambiente para testes
os.environ["SECRET_KEY"] = "test_secret_key_for_jwt_tokens_in_tests_should_be_very_secure"


# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
TEST_MONGO_URI = 'mongodb://localhost:27017'
TESTE_DB_NAME = 'SocialJAM_TEST'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a loop to deal with async functions
@pytest.fixture(scope='session')
def event_loop():
    # Allows you to run asynchronous tests with pytest-asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

# fixture for the mongoDB connection using a test db
@pytest_asyncio.fixture(scope="function")
async def mongo_client():
    # create a mongoDB client for the tests and then clean it after the tests
    client = AsyncIOMotorClient(TEST_MONGO_URI)
    db = client[TESTE_DB_NAME]
    yield db
    await client.drop_database(TESTE_DB_NAME)
    client.close() 

@pytest.fixture(scope="function")
def db_session():
    """Fixture que cria uma sessão de banco de dados para testes"""
    base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture que cria um cliente de teste do FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    # Mock MongoDB for tests with proper async interface
    def override_get_mongo():
        class MockMongoCollection:
            def __init__(self):
                self.data = []
            
            async def update_one(self, filter_dict, update_dict, upsert=False):
                # Mock implementation for update_one
                class MockResult:
                    def __init__(self):
                        self.upserted_id = "mock_id"
                        self.modified_count = 1
                        self.matched_count = 1
                return MockResult()
            
            async def find_one(self, filter_dict):
                # Mock implementation for find_one - return None (not found)
                return None
            
            async def insert_one(self, document):
                # Mock implementation for insert_one
                class MockResult:
                    def __init__(self):
                        self.inserted_id = "mock_id"
                return MockResult()
            
            async def find(self, filter_dict=None):
                # Mock implementation for find
                return []
            
            async def delete_one(self, filter_dict):
                # Mock implementation for delete_one
                class MockResult:
                    def __init__(self):
                        self.deleted_count = 1
                return MockResult()
        
        class MockMongoDB:
            def __init__(self):
                self.collections = {}
                
            def __getitem__(self, key):
                if key not in self.collections:
                    self.collections[key] = MockMongoCollection()
                return self.collections[key]
        
        return MockMongoDB()
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_mongo_db_with_check] = override_get_mongo
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Fixture com dados de exemplo para usuário"""
    return {
        "username": "testuser",
        "nome": "Test User",
        "email": "test@example.com",
        "senha": "testpassword123"
    }


@pytest.fixture
def sample_artist_data():
    """Fixture com dados de exemplo para artista"""
    return {
        "nome": "Test Artist",
        "music_genre": "Rock"
    }


@pytest.fixture
def sample_album_data():
    """Fixture com dados de exemplo para álbum"""
    return {
        "nome": "Test Album",
        "total_tracks": 10,
        "artist_id": 1
    }