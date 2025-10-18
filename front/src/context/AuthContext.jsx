import React, { createContext, useContext, useState, useEffect } from 'react';
import { isAuthenticated, getToken, logoutUser, getMe } from '@/api';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth deve ser usado dentro de um AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [user,setUser] = useState(null);

    useEffect(() => {
        const checkAuth = () => {
            const authenticated = isAuthenticated();
            setIsLoggedIn(authenticated);
            setIsLoading(false);
        };

        checkAuth();
    }, []);

    useEffect(() => { //essa função checa se o usuario ta autenticado
    const checkAuth = async () => {
        const authenticated = isAuthenticated();
        setIsLoggedIn(authenticated);
        
        if (authenticated) {
            await loadUserData();  //aí ela chama esse loadUserData que vai
        }                          //puxar as informações da api
        
        setIsLoading(false);
    };

    checkAuth();
    }, []);

    const login = () => {
        setIsLoggedIn(true);
    };

    const logout = () => {
        logoutUser();
        setIsLoggedIn(false);
    };

    const loadUserData = async () => { 
        const result = await getMe();
        if (result.success) {
            setUser(result.me); //aqui ele puxa as informações da api e "seta"
        }                       //a variavel user com o resultado
        };


    const value = {
        isLoggedIn,
        isLoading,
        user, //aqui ele passa ela pra uso
        login,
        logout,
        token: getToken(),
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};