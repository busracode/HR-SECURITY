import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children, roleRequired }) => {
    const { user } = useAuth();

    // 1. Giriş kontrolü
    if (!user) {
        return <Navigate to="/login" />;
    }

    // 2. Rol kontrolü (RBAC)
    if (roleRequired && user.role !== roleRequired) {
        return (
            <div style={{ padding: "20px", color: "red" }}>
                <h2>⛔ Erişim Reddedildi</h2>
                <p>Bu sayfayı sadece <strong>{roleRequired}</strong> yetkisine sahip kişiler görebilir.</p>
                <a href="/dashboard">Geri Dön</a>
            </div>
        );
    }

    return children;
};

export default ProtectedRoute;