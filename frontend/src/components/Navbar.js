import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const { user, logout } = useAuth();
    const { language, changeLanguage, t } = useLanguage();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const toggleLanguage = () => {
        changeLanguage(language === 'en' ? 'tr' : 'en');
    };

    return (
        <nav className="bg-white/80 backdrop-blur-xl border-b border-slate-200/50 shadow-[0_10px_30px_-10px_rgba(0,0,0,0.1)] sticky top-0 z-50 px-8 py-5 flex justify-between items-center transition-all duration-300">
            <div className="flex items-center gap-4 group cursor-pointer">
                <div className="bg-gradient-to-br from-blue-600 to-indigo-700 text-white font-black text-2xl p-3 rounded-2xl leading-none shadow-[0_8px_15px_rgba(79,70,229,0.3)] group-hover:scale-105 transition-transform">
                    İK
                </div>
                <span className="font-extrabold text-2xl text-transparent bg-clip-text bg-gradient-to-r from-slate-800 to-slate-600 tracking-tight drop-shadow-sm">
                    HR Güvenlik
                </span>
            </div>
            
            <div className="flex items-center gap-6">
                <button 
                    onClick={toggleLanguage}
                    className="font-bold text-slate-600 hover:text-blue-600 bg-slate-100 hover:bg-blue-50 px-3 py-2 rounded-xl transition-all shadow-sm border border-slate-200"
                >
                    {language === 'en' ? '🇹🇷 TR' : '🇬🇧 EN'}
                </button>

                {user ? (
                    <div className="flex items-center gap-6">
                        <div className="text-lg bg-slate-50 px-5 py-2 rounded-2xl shadow-inner border border-slate-100 flex items-center">
                            <span className="text-slate-500 font-medium mr-2">{t('navbar.welcome')}</span>
                            <span className="font-bold text-slate-800">{user.username || user.name}</span>
                            {user.role === 'Admin' && (
                                <span className="ml-3 bg-gradient-to-r from-purple-500 to-indigo-500 text-white text-sm font-bold px-3 py-1 rounded-lg shadow-md">
                                    {t('navbar.admin')}
                                </span>
                            )}
                        </div>
                        <button 
                            onClick={handleLogout}
                            className="text-lg font-bold text-white bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 px-6 py-3 rounded-xl shadow-[0_8px_15px_rgba(225,29,72,0.3)] hover:shadow-[0_12px_20px_rgba(225,29,72,0.4)] transform hover:-translate-y-1 transition-all duration-300"
                        >
                            {t('navbar.logout')}
                        </button>
                    </div>
                ) : (
                    <div className="flex gap-4">
                        <Link to="/login" className="text-lg font-bold text-slate-600 hover:text-blue-600 bg-slate-50 hover:bg-blue-50 px-6 py-3 rounded-xl transition-all shadow-sm">
                            {t('navbar.login')}
                        </Link>
                        <Link to="/register" className="text-lg font-bold bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-500 hover:to-indigo-500 px-6 py-3 rounded-xl shadow-[0_8px_15px_rgba(79,70,229,0.3)] hover:shadow-[0_12px_20px_rgba(79,70,229,0.4)] transform hover:-translate-y-1 transition-all duration-300">
                            {t('navbar.register')}
                        </Link>
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
