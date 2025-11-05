from sqlalchemy.orm import Session
from .. import models_sql, schemas
from ..database import get_db
from fastapi import Depends, status, HTTPException
from typing import List

def send_friend_request(sender_id: int, receiver_id: int, db: Session = Depends(get_db)):
    #Envia uma solicitação de amizade
    #verificar se os usuários existem
    sender = db.query(models_sql.User).filter(models_sql.User.id == sender_id).first()
    receiver = db.query(models_sql.User).filter(models_sql.User.id == receiver_id).first()
    
    if not sender or not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    #verificar se não é o mesmo usuário
    if sender_id == receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Você não pode enviar solicitação para si mesmo")
    
    #verificar se já existe uma solicitação pendente
    existing_request = db.query(models_sql.FriendRequest).filter(
        (models_sql.FriendRequest.sender_id == sender_id) & 
        (models_sql.FriendRequest.receiver_id == receiver_id) |
        (models_sql.FriendRequest.sender_id == receiver_id) & 
        (models_sql.FriendRequest.receiver_id == sender_id)
    ).first()
    
    if existing_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solicitação já existe")
    
    #verificar se já são amigos
    existing_friendship = db.query(models_sql.Friendship).filter(
        (models_sql.Friendship.user1_id == sender_id) & 
        (models_sql.Friendship.user2_id == receiver_id) |
        (models_sql.Friendship.user1_id == receiver_id) & 
        (models_sql.Friendship.user2_id == sender_id)
    ).first()
    
    if existing_friendship:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vocês já são amigos")
    
    #criar nova solicitação
    new_request = models_sql.FriendRequest(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status="Pending"
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    #criar notificação para o receptor
    notification = models_sql.Notification(
        user_id=receiver_id,
        type="friend_request",
        content=f"{sender.username} enviou uma solicitação de amizade",
        read=False
    )
    
    db.add(notification)
    db.commit()
    
    return new_request

def respond_to_friend_request(request_id: int, response: str, user_id: int, db: Session = Depends(get_db)):
    #Responde a uma solicitação de amizade (aceitar ou recusar)
    if response not in ["Accepted", "Denied"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resposta deve ser 'Accepted' ou 'Denied'")
    
    #buscar a solicitação
    friend_request = db.query(models_sql.FriendRequest).filter(
        models_sql.FriendRequest.id == request_id,
        models_sql.FriendRequest.receiver_id == user_id,
        models_sql.FriendRequest.status == "Pending"
    ).first()
    
    if not friend_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitação não encontrada ou já respondida")
    
    #atualizar status da solicitação
    friend_request.status = response
    db.commit()
    
    #se aceita, criar amizade
    if response == "Accepted":
        #garantir que user1_id seja sempre menor que user2_id para evitar duplicatas
        user1_id = min(friend_request.sender_id, friend_request.receiver_id)
        user2_id = max(friend_request.sender_id, friend_request.receiver_id)
        
        new_friendship = models_sql.Friendship(
            user1_id=user1_id,
            user2_id=user2_id
        )
        
        db.add(new_friendship)
        db.commit()
        db.refresh(new_friendship)
        
        #criar notificação para o remetente
        sender = db.query(models_sql.User).filter(models_sql.User.id == friend_request.sender_id).first()
        receiver = db.query(models_sql.User).filter(models_sql.User.id == friend_request.receiver_id).first()
        
        notification = models_sql.Notification(
            user_id=friend_request.sender_id,
            type="friend_request",
            content=f"{receiver.username} aceitou sua solicitação de amizade",
            read=False
        )
        
        db.add(notification)
        db.commit()
        
        return new_friendship
    
    return friend_request

def get_friend_requests(user_id: int, db: Session = Depends(get_db)):
    #busca solicitações de amizade recebidas pendentes
    requests = db.query(models_sql.FriendRequest).filter(
        models_sql.FriendRequest.receiver_id == user_id,
        models_sql.FriendRequest.status == "Pending"
    ).all()
    
    return requests

def get_sent_friend_requests(user_id: int, db: Session = Depends(get_db)):
    #busca solicitações de amizade enviadas pendentes
    requests = db.query(models_sql.FriendRequest).filter(
        models_sql.FriendRequest.sender_id == user_id,
        models_sql.FriendRequest.status == "Pending"
    ).all()
    
    return requests

def get_friends(user_id: int, db: Session = Depends(get_db)):
    #busca lista de amigos do usuário
    friendships = db.query(models_sql.Friendship).filter(
        (models_sql.Friendship.user1_id == user_id) | 
        (models_sql.Friendship.user2_id == user_id)
    ).all()
    
    friend_ids = []
    for friendship in friendships:
        if friendship.user1_id == user_id:
            friend_ids.append(friendship.user2_id)
        else:
            friend_ids.append(friendship.user1_id)
    
    #buscar informações dos amigos
    friends = db.query(models_sql.User).filter(models_sql.User.id.in_(friend_ids)).all()
    
    return friends

def remove_friend(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    #remove amizade entre dois usuários
    #garantir que user1_id seja sempre menor que user2_id
    user1_id = min(user_id, friend_id)
    user2_id = max(user_id, friend_id)
    
    friendship = db.query(models_sql.Friendship).filter(
        models_sql.Friendship.user1_id == user1_id,
        models_sql.Friendship.user2_id == user2_id
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Amizade não encontrada")
    
    db.delete(friendship)
    db.commit()
    
    return {"message": "Amizade removida com sucesso"}

def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    #busca notificações do usuário
    notifications = db.query(models_sql.Notification).filter(
        models_sql.Notification.user_id == user_id
    ).order_by(models_sql.Notification.created_at.desc()).all()
    
    return notifications

def mark_notification_as_read(notification_id: int, user_id: int, db: Session = Depends(get_db)):
    #marca notificação como lida
    notification = db.query(models_sql.Notification).filter(
        models_sql.Notification.id == notification_id,
        models_sql.Notification.user_id == user_id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificação não encontrada")
    
    notification.read = True
    db.commit()
    
    return notification

def search_users(query: str, current_user_id: int, db: Session = Depends(get_db)):
    #busca usuários por nome de usuário ou nome
    users = db.query(models_sql.User).filter(
        (models_sql.User.username.ilike(f"%{query}%") | 
         models_sql.User.nome.ilike(f"%{query}%")) &
        (models_sql.User.id != current_user_id)
    ).all()
    
    return users