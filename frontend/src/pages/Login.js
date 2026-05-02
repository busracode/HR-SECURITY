import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    const { login } = useAuth();
    const { t } = useLanguage();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await api.post('/login', { email, password });
            
            login(response.data);
            
            if (response.data.role === 'HR') {
                navigate('/admin');
            } else {
                navigate('/dashboard');
            }
            
            setLoading(false);
            
        } catch (err) {
            setError(err.response?.data?.message || t('login.error_generic'));
            setLoading(false);
        }
    };

    return (
        <div className="min-h-[calc(100vh-80px)] flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-blue-100 py-20 px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl w-full space-y-10 bg-white/80 backdrop-blur-xl p-14 rounded-[2.5rem] shadow-[0_30px_60px_-15px_rgba(0,0,0,0.15)] border-t border-l border-white">
                <div>
                    <h2 className="mt-2 text-center text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700 drop-shadow-sm">
                        {t('login.title')}
                    </h2>
                    <p className="mt-4 text-center text-lg text-slate-600 font-medium">
                        {t('login.or')}{' '}
                        <Link to="/register" className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 transition-all">
                            {t('login.register_link')}
                        </Link>
                    </p>
                </div>
                
                {error && (
                    <div className="bg-red-50 border-l-8 border-red-500 p-5 mb-4 rounded-xl shadow-md">
                        <p className="text-lg font-medium text-red-700">{error}</p>
                    </div>
                )}

                <form className="mt-10 space-y-8" onSubmit={handleSubmit}>
                    <div className="space-y-6">
                        <div>
                            <label className="block text-lg font-bold text-slate-700 mb-2 drop-shadow-sm" htmlFor="email">{t('login.email')}</label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                required
                                className="appearance-none rounded-2xl relative block w-full px-5 py-4 border-2 border-slate-200 placeholder-slate-400 text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-500/30 focus:border-blue-500 text-lg transition-all shadow-inner bg-slate-50 focus:bg-white font-medium"
                                placeholder="ornek@hr.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="block text-lg font-bold text-slate-700 mb-2 drop-shadow-sm" htmlFor="password">{t('login.password')}</label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                className="appearance-none rounded-2xl relative block w-full px-5 py-4 border-2 border-slate-200 placeholder-slate-400 text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-500/30 focus:border-blue-500 text-lg transition-all shadow-inner bg-slate-50 focus:bg-white font-medium"
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={loading}
                            className={`group relative w-full flex justify-center py-4 px-6 border border-transparent text-xl font-bold rounded-2xl text-white ${loading ? 'bg-blue-400 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-[0_10px_20px_rgba(79,70,229,0.3)] hover:shadow-[0_15px_30px_rgba(79,70,229,0.4)] hover:-translate-y-1'} focus:outline-none focus:ring-4 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform`}
                        >
                            {loading ? t('login.button_loading') : t('login.button')}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
