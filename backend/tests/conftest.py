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
from passlib.context import CryptContext

# Habilitar modo de testes ANTES de importar o app
os.environ["TESTING"] = "true"

from app.database import base, get_db
from app.core.mongo import get_mongo_db_with_check
from app.core.security import Hash
from main import app

# Criar contexto de criptografia para o mock
pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Banco totalmente em memória (CORRETO)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

TEST_MONGO_URI = 'mongodb://localhost:27017'
TESTE_DB_NAME = 'SocialJAM_TEST'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Necessário para manter uma única conexão
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_client():
    client = AsyncIOMotorClient(TEST_MONGO_URI)
    db = client[TESTE_DB_NAME]
    yield db
    await client.drop_database(TESTE_DB_NAME)
    client.close()


@pytest.fixture(scope="function")
def db_session():
    base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de teste com mocks de MongoDB e Hash.
    """
    def override_get_db():
        yield db_session

    # Mock MongoDB para testes
    def override_get_mongo():
        class MockMongoCollection:
            def __init__(self):
                self.data = []

            async def update_one(self, *a, **k):
                class R:
                    upserted_id = "mock_id"
                    modified_count = 1
                    matched_count = 1
                return R()

            async def find_one(self, *a, **k):
                return None

            async def insert_one(self, *a, **k):
                class R:
                    inserted_id = "mock_id"
                return R()

            async def find(self, *a, **k):
                return []

            async def delete_one(self, *a, **k):
                class R:
                    deleted_count = 1
                return R()

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

    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
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


@pytest.fixture(autouse=True)
def fast_hash(monkeypatch):
    """
    Mock de Hash para testes rápidos.
    Usa hash bcrypt válido para evitar erros de validação.
    """
    # Hash bcrypt real de "testpassword123" - mais rápido que gerar novo a cada teste
    FIXED_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYmPnr7u.3S"
    
    # Dicionário para armazenar senhas mockadas (senha original -> hash)
    password_store = {}
    
    def mock_hash(password):
        # Para testes, sempre retorna o mesmo hash válido
        # Mas armazena a relação senha->hash para verificação posterior
        password_store[password] = FIXED_HASH
        return FIXED_HASH
    
    def mock_verify(plain_pwd, hashed_pwd):
        # Se a senha foi hashada antes e o hash é o mesmo, retorna True
        if hashed_pwd == FIXED_HASH:
            # Em testes, qualquer senha que foi hashada é considerada válida
            # desde que seja a mesma que foi usada no hash
            return plain_pwd in password_store
        # Fallback para verificação real se necessário
        return pwd_cxt.verify(plain_pwd, hashed_pwd)
    
    monkeypatch.setattr(Hash, "hashPWD", mock_hash)
    monkeypatch.setattr(Hash, "verify", mock_verify)
