
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
    <CardUser nomeUsuario = {user?.nome} artistaFav = {user?.nome} ></CardUser>
    )
   
};

export default Profile;