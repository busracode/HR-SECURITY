import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const Dashboard = () => {
    const { user } = useAuth();
    const { t } = useLanguage();
    
    const [application, setApplication] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitLoading, setSubmitLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const [formData, setFormData] = useState({
        job: '',
        school: '',
        department: '',
        salary: ''
    });

    useEffect(() => {
        const fetchApplication = async () => {
            try {
                const response = await api.get('/candidate/application');
                if (response.data.application) {
                    setApplication(response.data.application);
                }
            } catch (err) {
                console.error("Error fetching application:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchApplication();
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setSubmitLoading(true);

        try {
            // Include first_name and last_name from the user context
            const payload = {
                first_name: user?.user?.first_name || user?.first_name || '',
                last_name: user?.user?.last_name || user?.last_name || '',
                ...formData
            };
            await api.post('/apply', payload);
            setSuccess('Başvurunuz başarıyla alındı!');
            
            // Re-fetch application
            const response = await api.get('/candidate/application');
            if (response.data.application) {
                setApplication(response.data.application);
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Başvuru sırasında bir hata oluştu.');
        } finally {
            setSubmitLoading(false);
        }
    };

    if (loading) {
        return <div className="p-20 text-center text-2xl font-bold text-slate-500 animate-pulse">{t('dashboard.loading') || 'Yükleniyor...'}</div>;
    }

    return (
        <div className="p-8 md:p-14 max-w-[90rem] mx-auto w-full min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
            <header className="mb-12 bg-white/70 backdrop-blur-md p-8 rounded-3xl shadow-[0_15px_40px_-15px_rgba(0,0,0,0.1)] border border-white">
                <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700 drop-shadow-sm">{t('dashboard.title')}</h1>
                <p className="text-xl text-slate-600 mt-3 font-medium">
                    {t('dashboard.subtitle').replace('{name}', `${user?.user?.first_name || user?.first_name} ${user?.user?.last_name || user?.last_name}`)}
                </p>
            </header>

            <div className="bg-white/80 backdrop-blur-xl rounded-[2.5rem] shadow-[0_30px_60px_-15px_rgba(0,0,0,0.15)] border-t border-l border-white overflow-hidden p-10">
                {application ? (
                    <div>
                        <h3 className="text-2xl font-bold text-slate-800 drop-shadow-sm mb-6">{t('dashboard.status_title')}</h3>
                        <div className="bg-green-50 border-l-8 border-green-500 p-6 rounded-2xl mb-8">
                            <p className="text-xl font-bold text-green-800">{t('dashboard.status_success')}</p>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
                                <p className="text-sm font-bold text-slate-500 mb-1">{t('dashboard.position')}</p>
                                <p className="text-xl font-black text-slate-800">{application.job}</p>
                            </div>
                            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
                                <p className="text-sm font-bold text-slate-500 mb-1">{t('dashboard.school')}</p>
                                <p className="text-xl font-black text-slate-800">{application.school}</p>
                            </div>
                            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
                                <p className="text-sm font-bold text-slate-500 mb-1">{t('dashboard.department')}</p>
                                <p className="text-xl font-black text-slate-800">{application.department}</p>
                            </div>
                            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200 relative overflow-hidden group">
                                <p className="text-sm font-bold text-slate-500 mb-1">{t('dashboard.salary_encrypted')}</p>
                                <p className="text-xl font-black text-slate-800 blur-[3px] group-hover:blur-none transition-all duration-300">
                                    {application.salary} ₺
                                </p>
                                <span className="absolute top-4 right-4 bg-slate-200 text-slate-600 text-xs font-bold px-2 py-1 rounded">AES 256</span>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div>
                        <h3 className="text-2xl font-bold text-slate-800 drop-shadow-sm mb-6">{t('dashboard.new_application')}</h3>
                        <div className="mb-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-l-8 border-blue-500 rounded-2xl shadow-sm">
                            <p className="text-lg text-blue-800 font-bold">{t('dashboard.security_notice')}</p>
                        </div>

                        {error && (
                            <div className="bg-red-50 border-l-8 border-red-500 p-5 mb-6 rounded-xl">
                                <p className="text-lg font-medium text-red-700">{error}</p>
                            </div>
                        )}
                        {success && (
                            <div className="bg-green-50 border-l-8 border-green-500 p-5 mb-6 rounded-xl">
                                <p className="text-lg font-medium text-green-700">{success}</p>
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-lg font-bold text-slate-700 mb-2">{t('dashboard.form_position')}</label>
                                    <input required type="text" name="job" value={formData.job} onChange={handleChange} className="w-full px-5 py-4 rounded-2xl border-2 border-slate-200 focus:ring-4 focus:ring-blue-500/30 outline-none font-medium bg-slate-50 focus:bg-white transition-all" placeholder="Frontend Developer" />
                                </div>
                                <div>
                                    <label className="block text-lg font-bold text-slate-700 mb-2">{t('dashboard.form_salary')}</label>
                                    <input required type="text" name="salary" value={formData.salary} onChange={handleChange} className="w-full px-5 py-4 rounded-2xl border-2 border-slate-200 focus:ring-4 focus:ring-blue-500/30 outline-none font-medium bg-slate-50 focus:bg-white transition-all" placeholder="50000" />
                                </div>
                                <div>
                                    <label className="block text-lg font-bold text-slate-700 mb-2">{t('dashboard.form_school')}</label>
                                    <input required type="text" name="school" value={formData.school} onChange={handleChange} className="w-full px-5 py-4 rounded-2xl border-2 border-slate-200 focus:ring-4 focus:ring-blue-500/30 outline-none font-medium bg-slate-50 focus:bg-white transition-all" placeholder="MIT" />
                                </div>
                                <div>
                                    <label className="block text-lg font-bold text-slate-700 mb-2">{t('dashboard.form_department')}</label>
                                    <input required type="text" name="department" value={formData.department} onChange={handleChange} className="w-full px-5 py-4 rounded-2xl border-2 border-slate-200 focus:ring-4 focus:ring-blue-500/30 outline-none font-medium bg-slate-50 focus:bg-white transition-all" placeholder="Computer Science" />
                                </div>
                            </div>
                            <button type="submit" disabled={submitLoading} className="mt-8 w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-xl py-5 rounded-2xl hover:-translate-y-1 hover:shadow-xl transition-all disabled:opacity-50 disabled:hover:-translate-y-0 disabled:hover:shadow-none">
                                {submitLoading ? t('dashboard.submit_loading') : t('dashboard.submit_button')}
                            </button>
                        </form>
                    </div>
                )}
            </div>

            {/* HR Upgrade Section */}
            <div className="mt-12 bg-white/60 backdrop-blur-md rounded-3xl shadow-sm border border-slate-200 p-8 max-w-2xl mx-auto">
                <h4 className="text-xl font-bold text-slate-700 mb-4 flex items-center gap-2">
                    <span>🏢</span> {t('dashboard.hr_upgrade_title')}
                </h4>
                <p className="text-slate-500 font-medium mb-6">{t('dashboard.hr_upgrade_desc')}</p>
                
                <form 
                    onSubmit={async (e) => {
                        e.preventDefault();
                        const code = e.target.elements.secret_code.value;
                        if (!code) return;
                        
                        try {
                            const res = await api.post('/hr/upgrade', { secret_code: code });
                            alert(res.data.message);
                            window.location.href = '/login'; // Force re-login
                        } catch (err) {
                            alert(err.response?.data?.error || 'Doğrulama başarısız!');
                        }
                    }} 
                    className="flex gap-4"
                >
                    <input 
                        type="password" 
                        name="secret_code"
                        placeholder={t('dashboard.hr_upgrade_placeholder')}
                        className="flex-1 px-5 py-3 rounded-xl border-2 border-slate-200 focus:ring-4 focus:ring-indigo-500/20 outline-none font-medium bg-slate-50 focus:bg-white transition-all"
                    />
                    <button type="submit" className="bg-slate-800 text-white font-bold px-6 py-3 rounded-xl hover:bg-slate-700 transition-colors">
                        {t('dashboard.hr_upgrade_button')}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Dashboard;
