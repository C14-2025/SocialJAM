
import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';
import CardUser from '@/components/shared/CardUser';
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";
import { uploadProfilePicture, spotifyLogin, hasSpotifyConnected } from '@/api';

const Profile = () => {
    const { user, isLoading, refreshUser } = useAuth();
    const navigate = useNavigate();
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [isConnectingSpotify, setIsConnectingSpotify] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    const handleSpotifyConnect = async () => {
        setIsConnectingSpotify(true);
        try {
            const result = await spotifyLogin(window.location.pathname);
            if (result.success && result.authUrl) {
                // Redireciona para a página de autenticação do Spotify
                window.location.href = result.authUrl;
            } else {
                alert('Erro ao conectar com Spotify: ' + result.error);
                setIsConnectingSpotify(false);
            }
        } catch  {
            alert('Erro ao conectar com Spotify');
            setIsConnectingSpotify(false);
        }
    };

    const handleSaveChanges = async () => { //faz o upload da foto e da um refresh
        if (selectedFile) {
            setIsUploading(true);
            const result = await uploadProfilePicture(selectedFile); 
            
            if (result.success) {
                // esse refresh basicamente chama o loaduserdata
                if (refreshUser) {
                    await refreshUser();
                }
                setIsDrawerOpen(false);
                setSelectedFile(null);
            } else {
                alert('Erro ao fazer upload da foto: ' + result.error);
            }
            setIsUploading(false);
        } else {
            setIsDrawerOpen(false);
        }
    };

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

    const isSpotifyConnected = hasSpotifyConnected(user);

    return(
        <div className="flex flex-1 min-h-screen bg-user bg-fixed">
            <div className="common-container">
                <CardUser 
                    image={user?.user_photo_url ? `http://localhost:8000/${user?.user_photo_url}` : null} 
                    nomeUsuario={user?.username} 
                    artistaFav={user?.favorite_artist || 'Não informado'}
                    showEditButton={true}
                    onEditClick={() => setIsDrawerOpen(true)}
                />
                
                <div className="mt-6 flex flex-col gap-4">
                    <div className="bg-dark-3 rounded-xl p-4">
                        <h3 className="h3-bold mb-2">Conexão Spotify</h3>
                        <p className="text-light-3 text-sm mb-4">
                            {isSpotifyConnected 
                                ? '✅ Conectado ao Spotify' 
                                : 'Conecte sua conta Spotify para importar seus artistas favoritos'}
                        </p>
                        <Button 
                            onClick={handleSpotifyConnect}
                            disabled={isConnectingSpotify}
                            className="bg-green-600 hover:bg-green-700 w-full"
                        >
                            {isConnectingSpotify ? 'Conectando...' : 
                             isSpotifyConnected ? '🔄 Reconectar ao Spotify' : '🎵 Conectar ao Spotify'}
                        </Button>
                    </div>
                </div>
            </div>
            
            <Drawer open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
                <DrawerContent className="max-w-md mx-auto">
                    <DrawerHeader className="pb-2">
                        <DrawerTitle>Editar Perfil</DrawerTitle>
                        <DrawerDescription>
                            Atualize suas informações de perfil
                        </DrawerDescription>
                    </DrawerHeader>
                    
                    <div className="px-4 pb-2 space-y-3 ">
                        <div className="space-y-1">
                            <label className="text-sm font-medium text-light-1">Nome de usuário</label>
                            <input 
                                type="text" 
                                defaultValue={user?.username}
                                disabled
                                className="w-full p-2 rounded-lg bg-dark-4 border border-dark-4 text-light-1 text-sm opacity-60 cursor-not-allowed"
                            />
                        </div>
                        
                        <div className="space-y-1">
                            <label className="text-sm font-medium text-light-1">Foto de perfil</label>
                            <input 
                                type="file" 
                                accept="image/*"
                                onChange={handleFileChange}
                                className="w-full p-2 rounded-lg bg-dark-4 border border-dark-4 text-light-1 text-sm file:mr-4 file:py-1 file:px-3 file:rounded file:border-0 file:text-sm file:bg-primary-500 file:text-white hover:file:bg-primary-600 file:cursor-pointer"
                            />
                            {selectedFile && (
                                <p className="text-xs text-light-3 mt-1">
                                    Arquivo selecionado: {selectedFile.name}
                                </p>
                            )}
                        </div>
                    </div>
                    
                    <DrawerFooter className="pt-2 gap-2">
                        <Button 
                            onClick={handleSaveChanges}
                            disabled={isUploading}
                            className="bg-primary-500 hover:bg-primary-600 h-10"
                        >
                            {isUploading ? 'Salvando...' : 'Salvar alterações'}
                        </Button>
                        <DrawerClose asChild>
                            <Button variant="outline" className="h-10">Cancelar</Button>
                        </DrawerClose>
                    </DrawerFooter>
                </DrawerContent>
            </Drawer>
        </div>
    )
   
};

export default Profile;