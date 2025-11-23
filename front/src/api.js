import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/sign-in";
    }
    return Promise.reject(error);
  }
);

export const loginUser = async (email, password) => {
  try {
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    const response = await api.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    const { access_token, token_type } = response.data;

    localStorage.setItem("access_token", access_token);

    return {
      success: true,
      token: access_token,
      token_type,
    };
  } catch (error) {
    console.error("Erro no login:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro no login",
    };
  }
};

export const logoutUser = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};

export const getToken = () => {
  return localStorage.getItem("access_token");
};

export const getAllArtists = async () => {
  try {
    const response = await api.get("/artist/");
    return {
      success: true,
      artists: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar artistas:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar artistas",
    };
  }
};

export const getUser = async (username) => {
  try {
    const response = await api.get(`/user/${username}`);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar usuário:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar usuário",
    };
  }
};

export const getUserById = async (userId) => {
  try {
    const response = await api.get(`/user/id/${userId}`);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar usuário por ID:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar usuário",
    };
  }
};

export const getMe = async () => {
  try {
    const response = await api.get("/user/me");
    return {
      success: true,
      me: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar informações do usuário:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "ERRO",
    };
  }
};

export const searchUsers = async (searchTerm) => {
  try {
    if (!searchTerm || searchTerm.trim() === "") {
      return {
        success: true,
        users: [],
      };
    }

    const response = await api.get(`/user/pesquisar/${searchTerm}`);
    return {
      success: true,
      users: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar usuários:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar usuários",
      users: [],
    };
  }
};

export const uploadProfilePicture = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/user/upload-photo", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao fazer upload da foto:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao fazer upload da foto",
    };
  }
};

export const updateFavoriteArtist = async (artistName) => {
  try {
    const response = await api.put("/user/me/favorite-artist", {
      artist_name: artistName,
    });

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao atualizar artista favorito:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao atualizar artista favorito",
    };
  }
};

export const sendFriendRequest = async (receiverId) => {
  try {
    const response = await api.post(`/friends/request/${receiverId}`);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao enviar solicitação de amizade:", error);
    return {
      success: false,
      error:
        error.response?.data?.detail || "Erro ao enviar solicitação de amizade",
    };
  }
};

export const getSentFriendRequests = async () => {
  try {
    const response = await api.get("/friends/requests/sent");
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar solicitações enviadas:", error);
    return {
      success: false,
      error:
        error.response?.data?.detail || "Erro ao buscar solicitações enviadas",
    };
  }
};

export const getFriends = async () => {
  try {
    const response = await api.get("/friends/");
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar amigos:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar amigos",
    };
  }
};

export const getReceivedFriendRequests = async () => {
  try {
    const response = await api.get("/friends/requests");
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar solicitações recebidas:", error);
    return {
      success: false,
      error:
        error.response?.data?.detail || "Erro ao buscar solicitações recebidas",
    };
  }
};

export const respondToFriendRequest = async (requestId, response) => {
  try {
    const result = await api.put(`/friends/request/${requestId}/${response}`);
    return {
      success: true,
      data: result.data,
    };
  } catch (error) {
    console.error("Erro ao responder solicitação:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao responder solicitação",
    };
  }
};

export const removeFriend = async (friendId) => {
  try {
    const result = await api.delete(`/friends/${friendId}`);
    return {
      success: true,
      data: result.data,
    };
  } catch (error) {
    console.error("Erro ao remover amizade:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao remover amizade",
    };
  }
};

export const spotifyLogin = async (redirectUrl = "/") => {
  try {
    // Chama a rota do backend que retorna a URL de autenticação em JSON
    const response = await api.get("/spotify/login", {
      params: { redirect_url: redirectUrl },
    });

    // O backend retorna {"auth_url": "https://..."}
    return {
      success: true,
      authUrl: response.data.auth_url,
    };
  } catch (error) {
    console.error("Erro ao iniciar login Spotify:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao conectar com Spotify",
    };
  }
};

/**
 * Busca os top artistas do usuário no Spotify
 * Requer que o usuário já tenha se autenticado com Spotify
 */
export const getSpotifyTopArtists = async () => {
  try {
    const response = await api.get("/spotify/top-artists");
    return {
      success: true,
      artists: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar artistas do Spotify:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar artistas",
      needsAuth: error.response?.status === 401,
    };
  }
};

export const searchSpotifyArtists = async (query) => {
  try {
    const response = await api.get("/spotify/search-artists", {
      params: { q: query },
    });
    return {
      success: true,
      artists: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar artistas no Spotify:", error);
    return {
      success: false,
      error:
        error.response?.data?.detail || "Erro ao buscar artistas no Spotify",
      needsAuth: error.response?.status === 401,
    };
  }
};

/**
 * Busca informações de um artista específico pelo ID do Spotify
 */
export const getSpotifyArtistById = async (artistId) => {
  try {
    const response = await api.get(`/spotify/artist/${artistId}`);
    return {
      success: true,
      artist: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar artista no Spotify:", error);
    return {
      success: false,
      error:
        error.response?.data?.detail || "Erro ao buscar artista no Spotify",
      needsAuth: error.response?.status === 401,
    };
  }
};

/**
 * Busca todos os álbuns dos artistas sincronizados
 */
export const getSpotifyAlbums = async () => {
  try {
    const response = await api.get("/spotify/albums");
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar álbuns do Spotify:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar álbuns",
    };
  }
};

/**
 * Verifica se o usuário tem tokens do Spotify salvos
 * (verifica se o campo spotify_user_token existe no usuário atual)
 */
export const hasSpotifyConnected = (user) => {
  return user?.spotify_user_token != null;
};

/**
 * Cria um novo post para um artista
 */
export const createPost = async (artistId, content, images) => {
  try {
    const formData = new FormData();
    formData.append("artist_id", artistId);
    formData.append("content", content);

    // Adicionar imagens ao FormData
    if (images && images.length > 0) {
      images.forEach((image) => {
        formData.append("images", image);
      });
    }

    const response = await api.post("/posts/create", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao criar post:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao criar post",
    };
  }
};

/**
 * Busca posts de um artista específico
 */
export const getPostsByArtist = async (artistId, pagination = 20) => {
  try {
    const response = await api.get(`/posts/artist/${artistId}`, {
      params: { pagination },
    });
    return {
      success: true,
      posts: response.data,
    };
  } catch (error) {
    console.error("Erro ao buscar posts do artista:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao buscar posts",
    };
  }
};

/**
 * Desconecta o Spotify limpando os tokens do usuário
 */
export const disconnectSpotify = async () => {
  try {
    const response = await api.delete("/spotify/disconnect");
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error("Erro ao desconectar Spotify:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao desconectar Spotify",
    };
  }
};

/**
 * Toggle like em um post (adiciona ou remove like)
 * Retorna se o post foi curtido (true) ou descurtido (false)
 */
export const toggleLikePost = async (postId) => {
  try {
    const response = await api.post(`/posts/${postId}/like`);
    return {
      success: true,
      liked: response.data.liked,
      message: response.data.message,
    };
  } catch (error) {
    console.error("Erro ao dar like no post:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Erro ao dar like no post",
    };
  }
};

export const getNotifications = async () => {
    try {
        const response = await api.get('/friends/notifications');
        return {
            success: true,
            data: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar notificações:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao buscar notificações'
        };
    }
};

export const markNotificationAsRead = async (notificationId) => {
    try {
        const response = await api.put(`/friends/notifications/${notificationId}/read`);
        return {
            success: true,
            data: response.data
        };
    } catch (error) {
        console.error('Erro ao marcar notificação como lida:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao marcar notificação como lida'
        };
    }
};



export default api;
