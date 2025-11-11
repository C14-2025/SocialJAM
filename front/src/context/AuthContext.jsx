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


    useEffect(() => { //essa função checa se o usuario ta autenticado
    const checkAuth = async () => {
        try{
            const authenticated = isAuthenticated();
            setIsLoggedIn(authenticated);
        
            if (authenticated) {
                await loadUserData();  //aí ela chama esse loadUserData que vai
            }                          //puxar as informações da api
        } catch (error){
            console.error('Erro:', error);
        } finally{
            setIsLoading(false);
        }
    };

    checkAuth();
    }, []);

    const login = async() => {
        setIsLoggedIn(true);
        await loadUserData();
    };

    const logout = () => {
        logoutUser();
        setIsLoggedIn(false);
    };

    const loadUserData = async () => { 
        try{    
            const result = await getMe();
            if (result.success) {
                setUser(result.me); //aqui ele puxa as informações da api e "seta"
            }else {                 //a variavel user com o resultado
                setUser(null);
            }
        } catch(error){
            setUser(null);
        }
    };

    const value = {
        isLoggedIn,
        isLoading,
        user, //aqui ele passa ela pra uso
        login,
        logout,
        refreshUser: loadUserData, 
        token: getToken(),
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};