import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css'; // ✅ Bootstrap CSS
import './index.css';
import App from './App';
import { AuthProvider } from './context/AuthContext'; // ✅ 로그인 상태 관리 context 추가

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>  {/* ✅ 로그인 Context로 감싸기 */}
      <App />
    </AuthProvider>
  </React.StrictMode>
);
