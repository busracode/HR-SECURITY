import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const AdminPanel = () => {
    const [stats, setStats] = useState({ totalEmployees: 0, activeLeaves: 0, alerts: 0 });
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(true);
    
    const { t } = useLanguage();

    useEffect(() => {
        const fetchAdminData = async () => {
            try {
                const statsResponse = await api.get('/admin/stats');
                const activitiesResponse = await api.get('/admin/activities');
                
                setStats(statsResponse.data);
                setActivities(activitiesResponse.data);
            } catch (error) {
                console.error("Error loading data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchAdminData();
    }, []);

    if (loading) {
        return <div className="p-20 text-center text-2xl font-bold text-slate-500 animate-pulse">{t('admin.loading')}</div>;
    }

    return (
        <div className="p-8 md:p-14 max-w-[90rem] mx-auto w-full min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
            <header className="mb-12 bg-white/70 backdrop-blur-md p-8 rounded-3xl shadow-[0_15px_40px_-15px_rgba(0,0,0,0.1)] border border-white flex flex-col md:flex-row justify-between items-start md:items-center">
                <div>
                    <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-indigo-800 drop-shadow-sm">{t('admin.title')}</h1>
                    <p className="text-lg text-slate-600 mt-3 font-medium">
                        {t('admin.subtitle')}
                    </p>
                </div>
                <div className="mt-4 md:mt-0 bg-gradient-to-r from-green-400 to-emerald-500 text-white px-6 py-3 rounded-2xl shadow-lg font-bold text-lg">
                    {t('admin.system_status')}
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                <div className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] border-t border-l border-white flex flex-col transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-lg font-bold text-slate-500 uppercase tracking-widest mb-4 drop-shadow-sm">{t('admin.total_employees')}</h3>
                    <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-blue-500 to-indigo-600 mt-auto drop-shadow-sm">{stats.totalEmployees}</p>
                </div>
                <div className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] border-t border-l border-white flex flex-col transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-lg font-bold text-slate-500 uppercase tracking-widest mb-4 drop-shadow-sm">{t('admin.active_leaves')}</h3>
                    <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-orange-400 to-red-500 mt-auto drop-shadow-sm">{stats.activeLeaves}</p>
                </div>
                <div className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] border-t border-l border-white flex flex-col transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-lg font-bold text-slate-500 uppercase tracking-widest mb-4 drop-shadow-sm">{t('admin.system_alerts')}</h3>
                    <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-green-400 to-emerald-600 mt-auto drop-shadow-sm">{stats.alerts}</p>
                </div>
            </div>

            <div className="bg-white/80 backdrop-blur-xl rounded-[2.5rem] shadow-[0_30px_60px_-15px_rgba(0,0,0,0.15)] border-t border-l border-white overflow-hidden">
                <div className="px-10 py-8 border-b border-slate-200 bg-gradient-to-r from-slate-50 to-white flex justify-between items-center">
                    <h3 className="text-2xl font-bold text-slate-800 drop-shadow-sm">{t('admin.recent_activities')}</h3>
                    <button className="text-lg text-blue-600 hover:text-blue-800 font-bold bg-blue-50 hover:bg-blue-100 px-5 py-2 rounded-xl transition-colors">{t('admin.view_all')}</button>
                </div>
                <ul className="divide-y divide-slate-100 bg-white">
                    {activities.length > 0 ? (
                        activities.map((activity, index) => (
                            <li key={index} className="px-10 py-6 flex items-center hover:bg-slate-50 transition-colors">
                                <span className={`w-4 h-4 rounded-full mr-6 shadow-md ${activity.type === 'login' ? 'bg-gradient-to-br from-blue-400 to-blue-600' : activity.type === 'security' ? 'bg-gradient-to-br from-green-400 to-green-600' : 'bg-gradient-to-br from-purple-400 to-purple-600'}`}></span>
                                <div>
                                    <p className="text-xl font-bold text-slate-800">{activity.description}</p>
                                    <p className="text-md font-medium text-slate-500 mt-1">{activity.time}</p>
                                </div>
                            </li>
                        ))
                    ) : (
                        <li className="px-10 py-16 text-center text-slate-500 text-xl font-medium bg-slate-50/50">
                            {t('admin.no_activity')}
                        </li>
                    )}
                </ul>
            </div>
        </div>
    );
};

export default AdminPanel;
