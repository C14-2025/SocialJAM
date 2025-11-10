
import React from 'react';
import { useAuth } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';
import CardUser from '@/components/shared/CardUser';
const Profile = () => {
    const { user, isLoading } = useAuth();
    const navigate = useNavigate();

    if (isLoading) {
        return (
            <div className="flex-center w-full h-screen">
                <div className="flex-center gap-2">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
                    Carregando
                </div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="flex-center w-full h-screen">
                <p>Erro ao carregar dados do perfil</p>
            </div>
        );
    }

    return(
    <CardUser image={user?.user_photo_url ? `http://localhost:8000/${user?.user_photo_url}` : null} nomeUsuario = {user?.username} artistaFav = {user?.nome} ></CardUser> //o ? retorna undefined caso n conseguir achar
    )
   
};

export default Profile;