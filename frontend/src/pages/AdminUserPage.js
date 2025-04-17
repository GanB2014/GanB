// src/pages/AdminUserPage.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const AdminUserPage = () => {
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);

  // ✅ 유저 목록 불러오기
  const fetchUsers = async () => {
    try {
      const res = await axios.get('http://localhost:8000/admin/users', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(res.data);
    } catch (err) {
      console.error('유저 불러오기 실패:', err);
    }
  };

  useEffect(() => {
    if (!user?.is_admin) {
      alert('접근 권한이 없습니다.');
      navigate('/');
      return;
    }
    fetchUsers();
  }, [user, token, navigate]);

  // ✅ 유저 정지 / 해제 처리
  const toggleBanUser = async (user_id, is_banned) => {
    const action = is_banned ? 'unban-user' : 'ban-user';
    try {
      await axios.patch(`http://localhost:8000/admin/${action}/${user_id}`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });
      await fetchUsers(); // 목록 갱신
    } catch (err) {
      alert('정지/해제 실패');
      console.error(err);
    }
  };

  // ✅ 유저 삭제
  const handleDeleteUser = async (user_id) => {
    const confirmDelete = window.confirm(`${user_id} 계정을 삭제하시겠습니까?`);
    if (!confirmDelete) return;

    try {
      await axios.delete(`http://localhost:8000/admin/users/${user_id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      await fetchUsers(); // 삭제 후 목록 갱신
    } catch (err) {
      console.error("삭제 실패:", err.response?.data || err.message);
      alert('❌ 삭제 실패: ' + (err.response?.data?.detail || '알 수 없는 오류'));
    }
  };

  return (
    <div className="container mt-4">
      {/* 게시글 목록으로 이동 버튼 */}
      <button onClick={() => navigate('/')} className="btn btn-outline-secondary mb-3">
        ← 게시글 목록으로
      </button>

      <h3>👥 전체 사용자 목록</h3>
      <table className="table table-bordered mt-3">
        <thead className="table-light">
          <tr>
            <th>ID</th>
            <th>아이디</th>
            <th>닉네임</th>
            <th>권한</th>
            <th>상태</th>
            <th>관리</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.user_id}</td>
              <td>{u.nickname}</td>
              <td>{u.is_admin ? '🛠 관리자' : '일반 사용자'}</td>
              <td>{u.is_banned ? '⛔ 정지됨' : '✅ 활성'}</td>
              <td>
                {!u.is_admin && (
                  <div className="d-flex gap-2">
                    <button
                      className={`btn btn-sm ${u.is_banned ? 'btn-success' : 'btn-danger'}`}
                      style={{ fontSize: '0.75rem', height: '28px', lineHeight: '1' }}
                      onClick={() => toggleBanUser(u.user_id, u.is_banned)}
                    >
                      {u.is_banned ? '해제' : '정지'}
                    </button>
                    <button
                      className="btn btn-sm btn-outline-danger"
                      style={{ fontSize: '0.75rem', height: '28px', lineHeight: '1' }}
                      onClick={() => handleDeleteUser(u.user_id)}
                    >
                      삭제
                    </button>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminUserPage;
