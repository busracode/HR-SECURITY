import React from 'react';

function App() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-blue-500">
      <div className="bg-white p-10 rounded-2xl shadow-2xl text-center">
        <h1 className="text-4xl font-extrabold text-blue-600 mb-4">
          İK Güvenlik Sistemi
        </h1>
        <p className="text-gray-600 text-lg">
          Tasarım ve Güvenlik Altyapısı Aktif!
        </p>
        <div className="mt-6 p-3 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 text-sm italic">
          🔒 Bcrypt & AES Hazırlıkları Tamamlandı.
        </div>
      </div>
    </div>
  );
}

export default App;