import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const AdminPanel = () => {
    const [stats, setStats] = useState({ totalCandidates: 0, pendingReviews: 0, alerts: 0 });
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [secretNote, setSecretNote] = useState('');
    const [savingNote, setSavingNote] = useState(false);
    
    const { t } = useLanguage();

    useEffect(() => {
        const fetchAdminData = async () => {
            try {
                const statsResponse = await api.get('/hr/stats').catch(() => ({ data: { totalCandidates: 0, pendingReviews: 0, alerts: 0 } }));
                const candidatesResponse = await api.get('/hr/candidates').catch(() => ({ data: [] }));
                
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

    const handleSaveNote = async (candidateId) => {
        setSavingNote(true);
        try {
            await api.post(`/hr/candidates/${candidateId}/note`, { note: secretNote });
            setCandidates(prev => prev.map(c => 
                c.id === candidateId ? { ...c, secret_note: secretNote } : c
            ));
            setSelectedCandidate(null);
            setSecretNote('');
            
            // Re-fetch stats to update pending reviews
            const statsResponse = await api.get('/hr/stats');
            setStats(statsResponse.data);
            
        } catch (error) {
            console.error("Error saving note:", error);
        } finally {
            setSavingNote(false);
        }
    };

    if (loading) {
        return <div className="p-20 text-center text-2xl font-bold text-slate-500 animate-pulse">{t('admin.loading') || 'Yükleniyor...'}</div>;
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
                        {t('admin.decryption_active')}
                    </div>
                </div>
                
                <div className="p-10">
                    {candidates.length > 0 ? (
                        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                            {candidates.map((candidate) => (
                                <div key={candidate.id} className="bg-slate-50 p-6 rounded-3xl shadow-inner border border-slate-100 flex flex-col justify-between">
                                    <div>
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h4 className="text-2xl font-extrabold text-slate-800">{candidate.name}</h4>
                                                <p className="text-md font-bold text-blue-600 bg-blue-100 px-3 py-1 rounded-lg inline-block mt-2">{candidate.position}</p>
                                            </div>
                                            <span className="bg-gradient-to-br from-slate-700 to-slate-900 text-white text-xs font-bold px-3 py-1.5 rounded-lg shadow-md flex items-center gap-2">
                                                <span>AES</span> 🔒
                                            </span>
                                        </div>
                                        
                                        <div className="bg-white p-4 rounded-2xl border-2 border-emerald-200 mb-4 shadow-sm relative overflow-hidden group">
                                            <div className="absolute top-0 right-0 bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-1 rounded-bl-lg">{t('admin.decrypted_salary')}</div>
                                            <p className="text-sm font-bold text-slate-500 mb-1">{t('admin.salary_label')}</p>
                                            <p className="font-mono font-black text-emerald-700 text-xl">
                                                {candidate.decrypted_salary} ₺
                                            </p>
                                        </div>

                                        <div className="mb-4">
                                            <p className="text-sm font-bold text-slate-500 mb-1">{t('admin.secret_note_label')}</p>
                                            <p className="text-slate-700 font-medium bg-indigo-50/50 p-4 rounded-2xl border border-indigo-100 italic">
                                                {candidate.secret_note ? `"${candidate.secret_note}"` : t('admin.no_note')}
                                            </p>
                                        </div>
                                    </div>
                                    
                                    <div className="mt-4 pt-4 border-t border-slate-200">
                                        {selectedCandidate === candidate.id ? (
                                            <div className="space-y-3">
                                                <textarea 
                                                    className="w-full bg-white border-2 border-indigo-200 rounded-xl p-3 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 font-medium"
                                                    rows="3"
                                                    placeholder={t('admin.note_placeholder')}
                                                    value={secretNote}
                                                    onChange={(e) => setSecretNote(e.target.value)}
                                                />
                                                <div className="flex gap-2">
                                                    <button 
                                                        onClick={() => handleSaveNote(candidate.id)}
                                                        disabled={savingNote}
                                                        className="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg shadow-md hover:bg-indigo-700 transition-colors flex-1"
                                                    >
                                                        {savingNote ? t('admin.saving_note') : t('admin.save_note')}
                                                    </button>
                                                    <button 
                                                        onClick={() => { setSelectedCandidate(null); setSecretNote(''); }}
                                                        className="bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-lg hover:bg-slate-300 transition-colors"
                                                    >
                                                        {t('admin.cancel')}
                                                    </button>
                                                </div>
                                            </div>
                                        ) : (
                                            <button 
                                                onClick={() => { setSelectedCandidate(candidate.id); setSecretNote(candidate.secret_note || ''); }}
                                                className="w-full text-indigo-600 font-bold py-3 border-2 border-indigo-100 rounded-xl hover:bg-indigo-50 transition-colors flex justify-center items-center gap-2"
                                            >
                                                {t('admin.add_note_btn')}
                                            </button>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-16">
                            <p className="text-2xl text-slate-400 font-bold mb-4">📭</p>
                            <p className="text-xl text-slate-500 font-medium">{t('admin.no_activity')}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminPanel;
