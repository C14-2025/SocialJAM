
import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
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
import { uploadProfilePicture, spotifyLogin, hasSpotifyConnected, searchSpotifyArtists, updateFavoriteArtist } from '@/api';

const Profile = () => {
    const { user, isLoading, refreshUser } = useAuth();
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [isConnectingSpotify, setIsConnectingSpotify] = useState(false);
    const [searchArtistValue, setSearchArtistValue] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [selectedArtist, setSelectedArtist] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    // Busca artistas ao digitar
    useEffect(() => {
        const trimmedValue = searchArtistValue.trim();

        if (!trimmedValue) {
            setSearchResults([]);
            setIsSearching(false);
            return;
        }

        let isActive = true;
        setIsSearching(true);

        const handler = setTimeout(async () => {
            try {
                const result = await searchSpotifyArtists(trimmedValue);
                if (!isActive) return;

                if (result.success && Array.isArray(result.artists)) {
                    setSearchResults(result.artists);
                } else {
                    setSearchResults([]);
                }
            } catch (error) {
                if (!isActive) return;
                setSearchResults([]);
                console.error("Erro ao buscar artistas:", error);
            } finally {
                if (isActive) {
                    setIsSearching(false);
                }
            }
        }, 400);

        return () => {
            isActive = false;
            clearTimeout(handler);
        };
    }, [searchArtistValue]);

    const handleArtistSelect = (artist) => {
        setSelectedArtist(artist);
        setSearchArtistValue(artist.name);
        setSearchResults([]);
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

    const handleSaveChanges = async () => {
        setIsUploading(true);
        let uploadSuccess = true;
        let artistSuccess = true;

        // Upload da foto se houver
        if (selectedFile) {
            const result = await uploadProfilePicture(selectedFile);
            if (!result.success) {
                alert('Erro ao fazer upload da foto: ' + result.error);
                uploadSuccess = false;
            }
        }

        // Atualizar artista favorito se houver
        if (selectedArtist) {
            const result = await updateFavoriteArtist(selectedArtist.name);
            if (!result.success) {
                alert('Erro ao atualizar artista favorito: ' + result.error);
                artistSuccess = false;
            }
        }

        // Se tudo deu certo, atualiza o usuário e fecha o drawer
        if (uploadSuccess && artistSuccess) {
            if (refreshUser) {
                await refreshUser();
            }
            setIsDrawerOpen(false);
            setSelectedFile(null);
            setSelectedArtist(null);
            setSearchArtistValue("");
        }
        
        setIsUploading(false);
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
                        
                        <div className="space-y-1 relative">
                            <label className="text-sm font-medium text-light-1">Artista Favorito</label>
                            <input 
                                type="text" 
                                value={searchArtistValue}
                                onChange={(e) => setSearchArtistValue(e.target.value)}
                                placeholder="Buscar artista..."
                                className="w-full p-2 rounded-lg bg-dark-4 border border-dark-4 text-light-1 text-sm focus:border-primary-500 outline-none"
                            />
                            {isSearching && (
                                <p className="text-xs text-light-3 mt-1">Buscando...</p>
                            )}
                            
                            {/* Resultados da busca */}
                            {searchResults.length > 0 && (
                                <div className="absolute z-10 w-full mt-1 bg-dark-3 rounded-lg border border-dark-4 max-h-48 overflow-y-auto">
                                    {searchResults.map((artist) => (
                                        <div
                                            key={artist.id}
                                            className="p-2 hover:bg-dark-4 cursor-pointer text-light-1 text-sm border-b border-dark-4 last:border-b-0"
                                            onClick={() => handleArtistSelect(artist)}
                                        >
                                            {artist.name}
                                        </div>
                                    ))}
                                </div>
                            )}
                            
                            {/* Artista selecionado */}
                            {selectedArtist && (
                                <div className="mt-2 p-2 bg-dark-4 rounded-lg flex items-center gap-3">
                                    <img 
                                        src={selectedArtist.photo || "/assets/icons/profile-placeholder.svg"} 
                                        alt={selectedArtist.name}
                                        className="w-12 h-12 rounded-lg object-cover"
                                    />
                                    <div className="flex-1">
                                        <p className="text-light-1 text-sm font-medium">{selectedArtist.name}</p>
                                        <p className="text-light-3 text-xs">{selectedArtist.followers} seguidores</p>
                                    </div>
                                    <button
                                        onClick={() => {
                                            setSelectedArtist(null);
                                            setSearchArtistValue("");
                                        }}
                                        className="text-light-3 hover:text-light-1"
                                    >
                                        ✕
                                    </button>
                                </div>
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