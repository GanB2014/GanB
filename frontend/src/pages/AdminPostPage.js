// src/pages/AdminPostPage.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AdminPostPage = () => {
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    if (!user?.is_admin) {
      alert('접근 권한이 없습니다.');
      navigate('/');
      return;
    }
    fetchPosts();
  }, [user, token]);

  const fetchPosts = async () => {
    try {
      const res = await axios.get('http://localhost:8000/posts/all', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPosts(res.data);
    } catch (err) {
      console.error('게시글 불러오기 실패:', err);
    }
  };

  const handleDeletePost = async (post_id) => {
    const confirmDelete = window.confirm(`게시글 ${post_id}을 삭제하시겠습니까?`);
    if (!confirmDelete) return;
    try {
      await axios.delete(`http://localhost:8000/admin/force-delete-post/${post_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchPosts(); // 목록 갱신
    } catch (err) {
      alert('삭제 실패');
      console.error(err);
    }
  };

  return (
    <div className="container mt-4">
      <h3>📝 게시글 관리</h3>
      <table className="table table-bordered mt-3">
        <thead className="table-light">
          <tr>
            <th>ID</th>
            <th>제목</th>
            <th>작성자</th>
            <th>관리</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post) => (
            <tr key={post.id}>
              <td>{post.id}</td>
              <td>{post.title}</td>
              <td>{post.nickname}</td>
              <td>
                <button
                  className="btn btn-sm btn-outline-danger"
                  onClick={() => handleDeletePost(post.id)}
                >
                  삭제
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPostPage;
