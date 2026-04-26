import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const AdminPanel = () => {
    const [stats, setStats] = useState({ totalCandidates: 0, pendingReviews: 0, alerts: 0 });
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(true);
    
    const { t } = useLanguage();

    useEffect(() => {
        const fetchAdminData = async () => {
            try {
                // Varsayılan istatistikler ve tüm aday listesi
                const statsResponse = await api.get('/admin/stats').catch(() => ({ data: { totalCandidates: 0, pendingReviews: 0, alerts: 0 } }));
                const candidatesResponse = await api.get('/admin/candidates').catch(() => ({ data: [] }));
                
                setStats(statsResponse.data);
                setCandidates(candidatesResponse.data);
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
                <div className="mt-4 md:mt-0 bg-gradient-to-r from-green-400 to-emerald-500 text-white px-6 py-3 rounded-2xl shadow-lg font-bold text-lg flex items-center gap-2">
                    <span className="w-3 h-3 bg-white rounded-full animate-pulse"></span>
                    {t('admin.system_status')}
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                <div className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] border-t border-l border-white flex flex-col transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-lg font-bold text-slate-500 uppercase tracking-widest mb-4 drop-shadow-sm">{t('admin.total_candidates')}</h3>
                    <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-blue-500 to-indigo-600 mt-auto drop-shadow-sm">{stats.totalCandidates}</p>
                </div>
                <div className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] border-t border-l border-white flex flex-col transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-lg font-bold text-slate-500 uppercase tracking-widest mb-4 drop-shadow-sm">{t('admin.pending_reviews')}</h3>
                    <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-orange-400 to-red-500 mt-auto drop-shadow-sm">{stats.pendingReviews}</p>
                </div>
                <div className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] border-t border-l border-white flex flex-col transform hover:-translate-y-2 transition-all duration-300">
                    <h3 className="text-lg font-bold text-slate-500 uppercase tracking-widest mb-4 drop-shadow-sm">{t('admin.security_alerts')}</h3>
                    <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-green-400 to-emerald-600 mt-auto drop-shadow-sm">{stats.alerts}</p>
                </div>
            </div>

            <div className="bg-white/80 backdrop-blur-xl rounded-[2.5rem] shadow-[0_30px_60px_-15px_rgba(0,0,0,0.15)] border-t border-l border-white overflow-hidden">
                <div className="px-10 py-8 border-b border-slate-200 bg-gradient-to-r from-slate-50 to-white flex justify-between items-center">
                    <h3 className="text-2xl font-bold text-slate-800 drop-shadow-sm">{t('admin.all_candidates')}</h3>
                    <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-lg font-bold text-sm border border-purple-200">
                        🔑 Tam Deşifre Yetkisi Aktif
                    </div>
                </div>
                
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50/50 text-slate-500 text-sm uppercase tracking-wider">
                                <th className="px-10 py-5 font-bold border-b border-slate-200">Aday Adı</th>
                                <th className="px-10 py-5 font-bold border-b border-slate-200">Pozisyon</th>
                                <th className="px-10 py-5 font-bold border-b border-slate-200">İnceleyen İK</th>
                                <th className="px-10 py-5 font-bold border-b border-slate-200">Maaş Beklentisi (Deşifre)</th>
                                <th className="px-10 py-5 font-bold border-b border-slate-200 text-right">Aksiyon</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-slate-100">
                            {candidates.length > 0 ? (
                                candidates.map((candidate, index) => (
                                    <tr key={index} className="hover:bg-slate-50 transition-colors group">
                                        <td className="px-10 py-6 font-extrabold text-slate-800 text-lg">{candidate.name}</td>
                                        <td className="px-10 py-6 font-bold text-slate-600">{candidate.position}</td>
                                        <td className="px-10 py-6 font-medium text-blue-600">{candidate.evaluator_name}</td>
                                        <td className="px-10 py-6 font-mono font-bold text-emerald-600 bg-emerald-50/30">
                                            {candidate.decrypted_salary ? `${candidate.decrypted_salary} ₺` : 'Bekleniyor...'}
                                        </td>
                                        <td className="px-10 py-6 text-right">
                                            <button className="text-indigo-600 hover:text-white font-bold bg-indigo-50 hover:bg-indigo-600 px-4 py-2 rounded-xl transition-all shadow-sm">
                                                {t('admin.view_details')}
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="5" className="px-10 py-16 text-center text-slate-500 text-xl font-medium bg-slate-50/50">
                                        {t('admin.no_activity')}
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AdminPanel;
