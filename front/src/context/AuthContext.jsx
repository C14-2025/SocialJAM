import React, { createContext, useContext, useState, useEffect } from 'react';
import { isAuthenticated, getToken, logoutUser } from '@/api';

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

    useEffect(() => {
        const checkAuth = () => {
            const authenticated = isAuthenticated();
            setIsLoggedIn(authenticated);
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

    const value = {
        isLoggedIn,
        isLoading,
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