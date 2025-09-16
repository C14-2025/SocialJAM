import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.posts_repository import PostsRepo
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

    post = await repo.get_post_by_id('68c70db5e711056c7db5e35c')

    assert post == None

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

    