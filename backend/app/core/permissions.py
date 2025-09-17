
from fastapi import HTTPException, status
from typing import Optional

class SystemPermissions: #Controla as permissões do sistema 
    @staticmethod
    def check_artist_creation_permission(is_system_script: bool = False): #Aqui checa se a criação de artistas é permitida
        if not is_system_script:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Criação de artistas não permitida. Artistas são importados automaticamente via Spotify."
            )
    
    @staticmethod
    def check_album_creation_permission(is_system_script: bool = False): #Aqui checa se a criação de álbuns é permitida
        if not is_system_script:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Criação de álbuns não permitida. Álbuns são importados automaticamente via Spotify."
            )
    
    @staticmethod
    def allow_system_operations():
        #No futuro, implementar verificação para o script do Spotify
        #Por enquanto, sempre retorna False (bloqueia todas as criações)
        return False


# Funções de conveniência para usar nas rotas
def require_system_script_for_artist_creation():
    #Dependência para bloquear criação de artistas por usuários
    SystemPermissions.check_artist_creation_permission(
        is_system_script=SystemPermissions.allow_system_operations()
    )

def require_system_script_for_album_creation():
    #Dependência para bloquear criação de álbuns por usuários
    SystemPermissions.check_album_creation_permission(
        is_system_script=SystemPermissions.allow_system_operations()
    )