import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        try {
            const storedUser = sessionStorage.getItem('user');
            if (storedUser && storedUser !== 'undefined') {
                return JSON.parse(storedUser);
            }
        } catch (error) {
            console.error("Session storage error on initialization:", error);
            // Hata durumunda hatalı veriyi temizle
            sessionStorage.removeItem('user');
            sessionStorage.removeItem('token');
        }
        return null;
    });

    const login = (userData) => {
        setUser(userData);
        sessionStorage.setItem('user', JSON.stringify(userData));
        if (userData.token) {
            sessionStorage.setItem('token', userData.token);
        }
    };

    const logout = () => {
        setUser(null);
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('token');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
