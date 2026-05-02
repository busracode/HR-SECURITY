import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const Sidebar = () => {
    const { user } = useAuth();
    const { t } = useLanguage();

    return (
        <aside className="w-80 bg-white/60 backdrop-blur-xl border-r border-slate-200/50 min-h-[calc(100vh-90px)] p-8 hidden md:flex flex-col shadow-[10px_0_30px_-15px_rgba(0,0,0,0.05)]">
            <div className="mb-10">
                <h2 className="text-sm font-black text-slate-400 uppercase tracking-widest mb-6 drop-shadow-sm">{t('sidebar.menu')}</h2>
                <nav className="flex flex-col gap-3">
                    {user?.role === 'Candidate' && (
                        <NavLink 
                            to="/dashboard" 
                            className={({ isActive }) => 
                                `px-6 py-4 rounded-2xl text-lg font-bold transition-all duration-300 transform ${
                                    isActive 
                                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_10px_20px_rgba(79,70,229,0.3)] hover:-translate-y-1' 
                                    : 'bg-slate-50 text-slate-600 hover:bg-white hover:text-blue-600 hover:shadow-md border border-transparent hover:border-slate-100'
                                }`
                            }
                        >
                            <div className="flex items-center gap-3">
                                <span className="text-xl">📊</span>
                                Aday Paneli
                            </div>
                        </NavLink>
                    )}
                    
                    {user?.role === 'HR' && (
                        <NavLink 
                            to="/admin" 
                            className={({ isActive }) => 
                                `px-6 py-4 rounded-2xl text-lg font-bold transition-all duration-300 transform mt-2 ${
                                    isActive 
                                    ? 'bg-gradient-to-r from-purple-600 to-indigo-700 text-white shadow-[0_10px_20px_rgba(124,58,237,0.3)] hover:-translate-y-1' 
                                    : 'bg-slate-50 text-slate-600 hover:bg-white hover:text-purple-600 hover:shadow-md border border-transparent hover:border-slate-100'
                                }`
                            }
                        >
                            <div className="flex items-center gap-3">
                                <span className="text-xl">⚙️</span>
                                İK Yönetimi
                            </div>
                        </NavLink>
                    )}
                </nav>
            </div>
            
            <div className="mt-auto pt-8 border-t border-slate-200/50">
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6 rounded-2xl shadow-[0_15px_30px_-10px_rgba(0,0,0,0.3)] text-white relative overflow-hidden">
                    <div className="absolute top-0 right-0 -mr-4 -mt-4 w-16 h-16 bg-blue-500 rounded-full opacity-20 blur-xl"></div>
                    <div className="absolute bottom-0 left-0 -ml-4 -mb-4 w-16 h-16 bg-purple-500 rounded-full opacity-20 blur-xl"></div>
                    
                    <div className="relative z-10">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="w-3 h-3 bg-green-400 rounded-full shadow-[0_0_10px_rgba(74,222,128,0.8)] animate-pulse"></span>
                            <p className="text-sm font-bold text-slate-300">{t('sidebar.secure_connection')}</p>
                        </div>
                        <p className="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                            AES-128
                        </p>
                        <p className="text-xs text-slate-400 mt-2 font-medium">{t('sidebar.encryption')}</p>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
