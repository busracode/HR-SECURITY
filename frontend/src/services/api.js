import axios from 'axios';

// Backend sunucusunun adresi (Şimdilik varsayılan 8000 olarak ayarlandı, gerekirse env'den çekilebilir)
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Her istekte (request) otomatik olarak Authorization header eklemek için Interceptor
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;
