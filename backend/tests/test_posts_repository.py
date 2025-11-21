import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from app.repositories.posts_repository import PostsRepo, PostNotFoundError
from app.models.mongo_posts import PostCreate
from bson.errors import InvalidId

@pytest.mark.asyncio
async def test_get_post_by_id_found():
    # define the waited response
    response = {
        '_id': '68c70db5e711056c7db5e35c',
        'author_id': 0,
        'content': 'Test',
        'likes': 0,
        'liked_by': [],
        'created_at': '2025-09-14 18:57:57.026249+00:00'
    }
    # create a mock for the method find_one of mongoDB lib
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = response

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)

    post = await repo.get_post_by_id('68c70db5e711056c7db5e35c')
    
    assert post == response

@pytest.mark.asyncio
async def test_get_post_by_id_not_found():
    # create a mock for the method find_one of mongoDB lib
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)

    with pytest.raises(PostNotFoundError):
        post = await repo.get_post_by_id('68c70db5e711056c7db5e35c')

@pytest.mark.asyncio
async def test_get_post_by_id_invalidID():
    # create a mock for the method find_one of mongoDB lib
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)

    with pytest.raises(InvalidId):
        post = await repo.get_post_by_id('123')

@pytest.mark.asyncio
async def test_create_post():
    inserted_id = '68c9c040619f5b84f887d6da'
    # create a mock for the method insert_onde of mongoDB lib
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.inserted_id = inserted_id
    mock_collection.insert_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)

    post = PostCreate(author_id='68c70db5e711056c7db5e35c', content='Test123', artist_id='artist123')

    assert await repo.create_post(post) == inserted_id

@pytest.mark.asyncio
async def test_creat_post_invalid_id():
    # create a mock for the method insert_onde of mongoDB lib
    mock_collection = AsyncMock()

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)

    post = PostCreate(author_id='123', content='Test123', artist_id='artist123')
    with pytest.raises(InvalidId):
        await repo.create_post(post)

@pytest.mark.asyncio
async def test_like_post_invalid_id():
    # create a mock for the method update_one of mongoDB lib
    mock_collection = AsyncMock()
    mock_collection.update_one.return_value = None

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)
    with pytest.raises(InvalidId):
        await repo.like_post('123', '68c70db5e711056c7db5e35c')
    
@pytest.mark.asyncio
async def test_delete_post_invalid_id():
    # create a mock for the method delete_one of mongoDB lib
    mock_collection = AsyncMock()
    mock_collection.update_one.return_value = None

    # create a mock object to make possibel to access using "db['Posts']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = PostsRepo(mock_db)

    with pytest.raises(InvalidId):
        await repo.delete_post('123')