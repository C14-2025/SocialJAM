from fastapi import APIRouter, Depends, status, HTTPException, Query
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..repositories import friends
from ..oauth2 import get_current_user

router = APIRouter(
    tags=['Friends'],
    prefix="/friends"
)

@router.post('/request/{receiver_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.FriendRequestOut)
def send_friend_request(
    receiver_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #envia uma solicitação de amizade
    return friends.send_friend_request(current_user.id, receiver_id, db)

@router.put('/request/{request_id}/{response}', status_code=status.HTTP_200_OK)
def respond_to_friend_request(
    request_id: int, 
    response: str,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #responde a uma solicitação de amizade (accepted ou denied)
    if response.lower() not in ["accepted", "denied"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Response deve ser 'accepted' ou 'denied'"
        )
    
    response_capitalized = response.capitalize()
    return friends.respond_to_friend_request(request_id, response_capitalized, current_user.id, db)

@router.get('/requests', status_code=status.HTTP_200_OK, response_model=List[schemas.FriendRequestOut])
def get_friend_requests(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #busca solicitações de amizade recebidas pendentes
    return friends.get_friend_requests(current_user.id, db)

@router.get('/requests/sent', status_code=status.HTTP_200_OK, response_model=List[schemas.FriendRequestOut])
def get_sent_friend_requests(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #busca solicitações de amizade enviadas pendentes
    return friends.get_sent_friend_requests(current_user.id, db)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_friends(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #busca lista de amigos do usuário
    return friends.get_friends(current_user.id, db)

@router.delete('/{friend_id}', status_code=status.HTTP_200_OK)
def remove_friend(
    friend_id: int,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #remove amizade com outro usuário
    return friends.remove_friend(current_user.id, friend_id, db)

@router.get('/search', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def search_users(
    q: str = Query(..., description="Termo de busca para nome de usuário ou nome"),
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #busca usuários por nome de usuário ou nome
    if len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Termo de busca deve ter pelo menos 2 caracteres"
        )
    return friends.search_users(q, current_user.id, db)

#rotas para notificações
@router.get('/notifications', status_code=status.HTTP_200_OK, response_model=List[schemas.NotificationOut])
def get_notifications(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #busca notificações do usuário
    return friends.get_user_notifications(current_user.id, db)

@router.put('/notifications/{notification_id}/read', status_code=status.HTTP_200_OK, response_model=schemas.NotificationOut)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #marca notificação como lida
    return friends.mark_notification_as_read(notification_id, current_user.id, db)

@router.get('/history', status_code=status.HTTP_200_OK, response_model=List[schemas.FriendRequestHistoryOut])
def get_friend_request_history(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    #busca histórico de solicitações de amizade do usuário
    return friends.get_friend_request_history(current_user.id, db)