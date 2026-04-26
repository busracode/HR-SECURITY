import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const Dashboard = () => {
    const { user } = useAuth();
    const { t } = useLanguage();
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedCandidate, setSelectedCandidate] = useState(null);
    const [secretNote, setSecretNote] = useState('');
    const [savingNote, setSavingNote] = useState(false);

    useEffect(() => {
        const fetchCandidates = async () => {
            try {
                const response = await api.get('/candidates');
                setCandidates(response.data);
            } catch (error) {
                console.error("Error fetching candidates:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchCandidates();
    }, []);

    const handleSaveNote = async (candidateId) => {
        if (!secretNote.trim()) return;
        setSavingNote(true);
        try {
            await api.post(`/candidates/${candidateId}/note`, { note: secretNote });
            // Optimistic update
            setCandidates(prev => prev.map(c => 
                c.id === candidateId ? { ...c, secret_note: secretNote } : c
            ));
            setSelectedCandidate(null);
            setSecretNote('');
        } catch (error) {
            console.error("Error saving note:", error);
        } finally {
            setSavingNote(false);
        }
    };

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
                <div className="px-10 py-8 border-b border-slate-200 bg-gradient-to-r from-slate-50 to-white flex justify-between items-center">
                    <h3 className="text-2xl font-bold text-slate-800 drop-shadow-sm">{t('dashboard.candidates_list')}</h3>
                    <button className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-2 px-6 rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all">
                        + {t('dashboard.new_candidate')}
                    </button>
                </div>
                
                <div className="p-10">
                    {loading ? (
                        <div className="text-center py-10 text-xl font-bold text-slate-500 animate-pulse">{t('dashboard.loading')}</div>
                    ) : candidates.length > 0 ? (
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
                                        
                                        <div className="bg-white p-4 rounded-2xl border-2 border-slate-200 mb-4 shadow-sm">
                                            <p className="text-sm font-bold text-slate-500 mb-1">{t('dashboard.salary_expectation')}</p>
                                            <p className="font-mono font-black text-slate-800 break-all text-sm blur-[2px] hover:blur-none transition-all duration-300 select-all cursor-crosshair">
                                                {candidate.encrypted_salary || 'b1g2k3j4h5g6f7d8s9a0...'}
                                            </p>
                                        </div>

                                        <div className="mb-4">
                                            <p className="text-sm font-bold text-slate-500 mb-1">{t('dashboard.secret_note')}</p>
                                            <p className="text-slate-700 font-medium bg-indigo-50/50 p-4 rounded-2xl border border-indigo-100 italic">
                                                {candidate.secret_note ? `"${candidate.secret_note}"` : "Henüz not eklenmemiş."}
                                            </p>
                                        </div>
                                    </div>
                                    
                                    <div className="mt-4 pt-4 border-t border-slate-200">
                                        {selectedCandidate === candidate.id ? (
                                            <div className="space-y-3">
                                                <textarea 
                                                    className="w-full bg-white border-2 border-indigo-200 rounded-xl p-3 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 font-medium"
                                                    rows="3"
                                                    placeholder="Aday hakkında gizli İK notunuz..."
                                                    value={secretNote}
                                                    onChange={(e) => setSecretNote(e.target.value)}
                                                />
                                                <div className="flex gap-2">
                                                    <button 
                                                        onClick={() => handleSaveNote(candidate.id)}
                                                        disabled={savingNote}
                                                        className="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg shadow-md hover:bg-indigo-700 transition-colors flex-1"
                                                    >
                                                        {savingNote ? '...' : t('dashboard.save_note')}
                                                    </button>
                                                    <button 
                                                        onClick={() => { setSelectedCandidate(null); setSecretNote(''); }}
                                                        className="bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-lg hover:bg-slate-300 transition-colors"
                                                    >
                                                        İptal
                                                    </button>
                                                </div>
                                            </div>
                                        ) : (
                                            <button 
                                                onClick={() => { setSelectedCandidate(candidate.id); setSecretNote(candidate.secret_note || ''); }}
                                                className="w-full text-indigo-600 font-bold py-3 border-2 border-indigo-100 rounded-xl hover:bg-indigo-50 transition-colors flex justify-center items-center gap-2"
                                            >
                                                📝 {t('dashboard.add_note')}
                                            </button>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-16">
                            <p className="text-2xl text-slate-400 font-bold mb-4">📭</p>
                            <p className="text-xl text-slate-500 font-medium">{t('dashboard.empty_list')}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
