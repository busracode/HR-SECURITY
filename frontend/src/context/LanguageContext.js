import React, { createContext, useState, useContext, useEffect } from 'react';
import { translations } from '../utils/translations';

const LanguageContext = createContext(null);

export const LanguageProvider = ({ children }) => {
    // Varsayılan dili localStorage'dan al, yoksa 'en' kullan
    const [language, setLanguage] = useState(() => {
        const storedLang = localStorage.getItem('language');
        return storedLang ? storedLang : 'en';
    });

    // Dil değiştiğinde localStorage'a kaydet
    useEffect(() => {
        localStorage.setItem('language', language);
    }, [language]);

    const changeLanguage = (lang) => {
        if (lang === 'en' || lang === 'tr') {
            setLanguage(lang);
        }
    };

    // Çeviri fonksiyonu
    const t = (key) => {
        return translations[language][key] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, changeLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => useContext(LanguageContext);
