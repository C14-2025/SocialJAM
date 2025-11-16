import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:8000"
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
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
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/sign-in';
        }
        return Promise.reject(error);
    }
);

export const loginUser = async (email, password) => {
    try {
        
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await api.post('/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        const { access_token, token_type } = response.data;
        
        localStorage.setItem('access_token', access_token);
        
        return {
            success: true,
            token: access_token,
            token_type
        };
    } catch (error) {
        console.error('Erro no login:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro no login'
        };
    }
};

export const logoutUser = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
};

export const isAuthenticated = () => {
    return !!localStorage.getItem('access_token');
};

export const getToken = () => {
    return localStorage.getItem('access_token');
};

export const getAllArtists = async () => {
    try {
        const response = await api.get('/artist/');
        return {
            success: true,
            artists: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar artistas:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao buscar artistas'
        };
    }
};

export const getUser = async () => {
    try {
        const response = await api.get('');
        return {
            success: true,
            artists: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar usuarios:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao buscar usuarios'
        };
    }
};

export const getMe= async () => {
    try {
        const response = await api.get('/user/me');
        return {
            success: true,
            me: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar informações do usuário:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'ERRO'
        };
    }
};

export const searchUsers = async (searchTerm) => {
    try {
        if (!searchTerm || searchTerm.trim() === '') {
            return {
                success: true,
                users: []
            };
        }
        
        const response = await api.get(`/user/pesquisar/${searchTerm}`);
        return {
            success: true,
            users: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar usuários:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao buscar usuários',
            users: []
        };
    }
};

export const uploadProfilePicture = async (file) => {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post('/user/upload-photo', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return {
            success: true,
            data: response.data
        };
    } catch (error) {
        console.error('Erro ao fazer upload da foto:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao fazer upload da foto'
        };
    }
};

export const sendFriendRequest = async (receiverId) => {
    try {
        const response = await api.post(`/friends/request/${receiverId}`);
        return {
            success: true,
            data: response.data
        };
    } catch (error) {
        console.error('Erro ao enviar solicitação de amizade:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao enviar solicitação de amizade'
        };
    }
};

export const getSentFriendRequests = async () => {
    try {
        const response = await api.get('/friends/requests/sent');
        return {
            success: true,
            data: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar solicitações enviadas:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao buscar solicitações enviadas'
        };
    }
};

export const getFriends = async () => {
    try {
        const response = await api.get('/friends/');
        return {
            success: true,
            data: response.data
        };
    } catch (error) {
        console.error('Erro ao buscar amigos:', error);
        return {
            success: false,
            error: error.response?.data?.detail || 'Erro ao buscar amigos'
        };
    }
};



export default api;