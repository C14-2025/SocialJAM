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


export default api;