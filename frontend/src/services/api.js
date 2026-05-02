import axios from 'axios';

// Backend sunucusunun adresi (Şimdilik varsayılan 8000 olarak ayarlandı, gerekirse env'den çekilebilir)
const API_URL = process.env.REACT_APP_API_URL || `http://${window.location.hostname}:5000`;

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

// Gelen yanıtlarda (response) 401 yetkisiz erişim hatalarını yakalamak için Interceptor
api.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response && error.response.status === 401) {
        // Token süresi dolmuş veya geçersizse otomatik çıkış yap
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
    return Promise.reject(error);
});

export default api;
