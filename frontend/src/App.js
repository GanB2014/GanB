import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PostList from './pages/PostList';
import PostDetail from './components/PostDetail';
import MyProfile from './pages/MyProfile';
import CreatePost from './pages/CreatePost';
import EditPost from './pages/EditPost';
import Register from './pages/Register';
import Notifications from './pages/Notifications';
import AdminUserPage from './pages/AdminUserPage';

function App() {
  return (
    <div className="min-h-screen bg-white text-black">
      <Router>
        <div className="p-8">
          <Routes>
            <Route path="/" element={<PostList />} />
            <Route path="/posts/:id" element={<PostDetail />} />
            <Route path="/profile" element={<MyProfile />} />
            <Route path="/create" element={<CreatePost />} />
            <Route path="/edit/:id" element={<EditPost />} />
            <Route path="/register" element={<Register />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/admin/users" element={<AdminUserPage />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
