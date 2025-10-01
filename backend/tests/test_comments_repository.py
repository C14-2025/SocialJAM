import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from app.repositories.comments_repository import CommentsRepo, CommentNotFoundError
from app.models.mongo_posts import CommentCreate
from bson.errors import InvalidId
from bson import ObjectId

@pytest.mark.asyncio
async def test_create_comment():
    inserted_id = '68c9c040619f5b84f887d6da'
    # create a mock for the method insert_one of mongoDB lib
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.inserted_id = inserted_id
    mock_collection.insert_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    comment = CommentCreate(post_id='68d4518661154a43266661b3', author_id='68c70db5e711056c7db5e35c', content='TEST_CONTENT')

    assert await repo.create_comment(comment) == inserted_id

@pytest.mark.asyncio
async def test_create_comment_with_wrong_ids():
    inserted_id = '68c9c040619f5b84f887d6da'
    # create a mock for the method insert_one of mongoDB lib
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.inserted_id = inserted_id
    mock_collection.insert_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    comment = CommentCreate(post_id='123', author_id='123', content='TEST_CONTENT')

    with pytest.raises(InvalidId):
        comment = await repo.create_comment(comment)

@pytest.mark.asyncio
async def test_get_comment_by_id():
    response = {
        '_id': '68c70db5e711056c7db5e35c',
        'post_id': 0,
        'author_id': 0,
        'content': 'Test',
        'likes': 0,
        'liked_by': [],
        'created_at': '2025-09-14 18:57:57.026249+00:00'
    }
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = response

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    comment = await repo.get_comment_by_id('68c70db5e711056c7db5e35c')

    assert comment == response

@pytest.mark.asyncio
async def test_get_comment_by_id_comment_not_found():
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(CommentNotFoundError):
        comment = await repo.get_comment_by_id('68c70db5e711056c7db5e35c')

@pytest.mark.asyncio
async def test_get_comment_by_id_wrong_id():
    
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = None

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(InvalidId):
        comment = await repo.get_comment_by_id('123')

@pytest.mark.asyncio
async def test_like_comment_not_found():
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.modified_count = 0
    mock_collection.update_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(CommentNotFoundError):
        await repo.like_comment('68c70db5e711056c7db5e35c', '68c9c040619f5b84f887d6da')

@pytest.mark.asyncio
async def test_like_comment_invalid_ids():
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.modified_count = 0
    mock_collection.update_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(InvalidId):
        await repo.like_comment('123', '123')

@pytest.mark.asyncio
async def test_get_post_comments():
    db_response = [
        {
            '_id': ObjectId('68d44ffa3bf8996a42b85dd5'),
            'post_id': ObjectId('68c9c040619f5b84f887d6da'),
            'author_id': ObjectId('68c70db5e711056c7db5e35c'),
            'content': 'Test',
            'likes': 1,
            'liked_by': [
                ObjectId('68c70db5e711056c7db5e35c')
            ],
            'created_at': '2025-09-14 18:57:57.026249+00:00'
        },
        {
            '_id': ObjectId('68d44ffa3bf8996a42b85dd5'),
            'post_id': ObjectId('68c9c040619f5b84f887d6da'),
            'author_id': ObjectId('68c70db5e711056c7db5e35c'),
            'content': 'Test_2',
            'likes': 1,
            'liked_by': [
                ObjectId('68c70db5e711056c7db5e35c')
            ],
            'created_at': '2025-09-14 18:57:57.026249+00:00'
        }
    ]

    expected = [
        {
            '_id': '68d44ffa3bf8996a42b85dd5',
            'post_id': '68c9c040619f5b84f887d6da',
            'author_id': '68c70db5e711056c7db5e35c',
            'content': 'Test',
            'likes': 1,
            'liked_by': [
                '68c70db5e711056c7db5e35c'
            ],
            'created_at': '2025-09-14 18:57:57.026249+00:00'
        },
        {
            '_id': '68d44ffa3bf8996a42b85dd5',
            'post_id': '68c9c040619f5b84f887d6da',
            'author_id': '68c70db5e711056c7db5e35c',
            'content': 'Test_2',
            'likes': 1,
            'liked_by': [
                '68c70db5e711056c7db5e35c'
            ],
            'created_at': '2025-09-14 18:57:57.026249+00:00'
        }
    ]

    # create a mock for the mongoDB lib obj
    mock_collection = Mock()
    return_mock = AsyncMock()
    return_mock.to_list.return_value = db_response
    mock_collection.find.return_value.sort.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    comments = await repo.get_post_comments('68c9c040619f5b84f887d6da')

    assert comments == expected

@pytest.mark.asyncio
async def test_get_post_comments_wrong_id():
    
    # create a mock for the mongoDB lib obj
    mock_collection = Mock()
    return_mock = AsyncMock()
    return_mock.to_list.return_value = None
    mock_collection.find.return_value.sort.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(InvalidId):
        comments = await repo.get_post_comments('123')

@pytest.mark.asyncio
async def test_delete_comment_not_found():
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.deleted_count = 0
    mock_collection.delete_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(CommentNotFoundError):
        await repo.delete_comment('68c70db5e711056c7db5e35c')

@pytest.mark.asyncio
async def test_delete_comment_not_found():
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.deleted_count = 1
    mock_collection.delete_one.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(InvalidId):
        await repo.delete_comment('123')

@pytest.mark.asyncio
async def test_on_post_deleted():
    expected = 15
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.deleted_count = expected
    mock_collection.delete_many.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    deleted = await repo.on_post_deleted('68c70db5e711056c7db5e35c')

    assert deleted == expected

@pytest.mark.asyncio
async def test_on_post_deleted_wrong_id():
    # create a mock for the mongoDB lib obj
    mock_collection = AsyncMock()
    return_mock = Mock()
    return_mock.deleted_count = None
    mock_collection.delete_many.return_value = return_mock

    # create a mock object to make possibel to access using "db['Comments']"
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    repo = CommentsRepo(mock_db)

    with pytest.raises(InvalidId):
        deleted = await repo.on_post_deleted('123')

    