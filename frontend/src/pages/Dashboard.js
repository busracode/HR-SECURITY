import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const Dashboard = () => {
    const { user } = useAuth();
    const { t } = useLanguage();

    return (
        <div className="p-8 md:p-14 max-w-[90rem] mx-auto w-full min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
            <header className="mb-12 bg-white/70 backdrop-blur-md p-8 rounded-3xl shadow-[0_15px_40px_-15px_rgba(0,0,0,0.1)] border border-white">
                <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700 drop-shadow-sm">{t('dashboard.title')}</h1>
                <p className="text-xl text-slate-600 mt-3 font-medium">{t('dashboard.subtitle')}</p>
            </header>

            <div className="mb-12 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-l-8 border-blue-500 rounded-2xl shadow-lg transform transition-all hover:scale-[1.01]">
                <div className="flex items-center">
                    <div className="flex-shrink-0">
                        <span className="text-3xl filter drop-shadow-md">🔒</span>
                    </div>
                    <div className="ml-5">
                        <p className="text-lg text-blue-800 font-bold drop-shadow-sm">
                            {t('dashboard.security_notice')}
                        </p>
                    </div>
                </div>
            </div>

            <div className="bg-white/80 backdrop-blur-xl rounded-[2.5rem] shadow-[0_30px_60px_-15px_rgba(0,0,0,0.15)] border-t border-l border-white overflow-hidden">
                <div className="px-10 py-8 border-b border-slate-200 bg-gradient-to-r from-slate-50 to-white">
                    <h3 className="text-2xl font-bold text-slate-800 drop-shadow-sm">{t('dashboard.personal_info')}</h3>
                </div>
                <div className="p-10">
                    <dl className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-10">
                        <div className="sm:col-span-1 bg-slate-50 p-6 rounded-2xl shadow-inner border border-slate-100">
                            <dt className="text-lg font-bold text-slate-500 mb-2">{t('dashboard.name')}</dt>
                            <dd className="mt-1 text-2xl text-slate-900 font-extrabold">{user?.username || t('dashboard.not_specified')}</dd>
                        </div>
                        <div className="sm:col-span-1 bg-slate-50 p-6 rounded-2xl shadow-inner border border-slate-100">
                            <dt className="text-lg font-bold text-slate-500 mb-2">{t('dashboard.email')}</dt>
                            <dd className="mt-1 text-xl text-slate-900 font-bold">{user?.email || t('dashboard.not_specified')}</dd>
                        </div>
                        <div className="sm:col-span-1 bg-slate-50 p-6 rounded-2xl shadow-inner border border-slate-100">
                            <dt className="text-lg font-bold text-slate-500 mb-2">{t('dashboard.role')}</dt>
                            <dd className="mt-1">
                                <span className="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-extrabold bg-gradient-to-r from-green-400 to-emerald-500 text-white shadow-md">
                                    {user?.role === 'Admin' ? t('dashboard.role_admin') : t('dashboard.role_employee')}
                                </span>
                            </dd>
                        </div>
                        <div className="sm:col-span-1 bg-slate-50 p-6 rounded-2xl shadow-inner border border-slate-100">
                            <dt className="text-lg font-bold text-slate-500 mb-2">{t('dashboard.department')}</dt>
                            <dd className="mt-1 text-xl text-slate-900 font-bold">{user?.department || t('dashboard.not_specified')}</dd>
                        </div>
                        <div className="sm:col-span-2 bg-slate-50 p-6 rounded-2xl shadow-inner border border-slate-100">
                            <dt className="text-lg font-bold text-slate-500 mb-3">{t('dashboard.iban')}</dt>
                            <dd className="mt-1 text-xl font-mono font-bold text-slate-800 bg-white p-5 rounded-xl border-2 border-slate-200 shadow-sm">
                                {user?.iban || t('dashboard.no_data')}
                            </dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
