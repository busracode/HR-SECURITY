import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* Herkesin erişebildiği korumalı alan */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />

        {/* Sadece İK (Admin) erişebildiği alan */}
        <Route path="/admin" element={
          <ProtectedRoute roleRequired="Admin">
            <AdminPanel />
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;