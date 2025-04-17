// src/pages/PostList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import NotificationDropdown from '../components/NotificationDropdown';

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [order, setOrder] = useState('newest');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const { user, login, logout } = useAuth();
  const [form, setForm] = useState({ user_id: '', password: '' });
  const navigate = useNavigate();

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async (page = 1, searchKeyword = '', sortOrder = 'newest') => {
    try {
      const res = await axios.get('http://localhost:8000/posts/', {
        params: {
          page,
          page_size: 10,
          ...(searchKeyword && { keyword: searchKeyword }),
          order: sortOrder,
        },
      });
      setPosts(res.data.posts);
      setCurrentPage(res.data.current_page);
      setTotalPages(res.data.total_pages);
    } catch (err) {
      console.error('게시글 불러오기 실패:', err);
    }
  };

  const handleSearchChange = (e) => setKeyword(e.target.value);
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') fetchPosts(1, keyword, order);
  };
  const handleOrderChange = (e) => {
    const value = e.target.value;
    setOrder(value);
    fetchPosts(1, keyword, value);
  };
  const handleSearchButtonClick = () => {
    fetchPosts(1, keyword, order);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/auth/login', {
        user_id: form.user_id,
        password: form.password,
      });
      login(res.data.access_token);
      setForm({ user_id: '', password: '' });
    } catch (err) {
      if (err.response && err.response.status === 403) {
        alert('정지된 계정입니다. 관리자에게 문의하세요.');
      } else {
        alert('로그인 실패: 아이디 또는 비밀번호 오류');
      }
    }
  };

  const handlePageChange = (pageNum) => {
    fetchPosts(pageNum, keyword, order);
  };

  return (
    <div className="container mt-4">
      {/* 🏠 헤더 */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="text-primary m-0">GanB</h1>

        {!user ? (
          <form className="d-flex gap-2 align-items-center" onSubmit={handleLogin}>
            <input
              type="text"
              name="user_id"
              value={form.user_id}
              onChange={handleChange}
              className="form-control form-control-sm"
              placeholder="ID"
              style={{ width: '120px' }}
            />
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="form-control form-control-sm"
              placeholder="PW"
              style={{ width: '120px' }}
            />
            <button type="submit" className="btn btn-sm btn-outline-primary" style={{ height: '28px', fontSize: '0.75rem' }}>
              로그인
            </button>
            <button
              type="button"
              className="btn btn-sm btn-outline-secondary"
              style={{ height: '28px', fontSize: '0.75rem' }}
              onClick={() => navigate('/register')}
            >
              회원가입
            </button>
          </form>
        ) : (
          <div className="text-end">
            <div className="fw-bold">{user.nickname} 님</div>
            <div className="d-flex justify-content-end gap-2 mt-1">
              <NotificationDropdown buttonStyle={{ height: '28px', fontSize: '0.75rem', padding: '2px 8px' }} />
              <button
                className="btn btn-outline-dark btn-sm"
                style={{ height: '28px', fontSize: '0.75rem', padding: '2px 8px' }}
                onClick={() => navigate('/profile')}
              >
                👤 프로필
              </button>
              <button
                className="btn btn-outline-danger btn-sm"
                style={{ height: '28px', fontSize: '0.75rem', padding: '2px 8px' }}
                onClick={logout}
              >
                🚪 로그아웃
              </button>
              {Boolean(user?.is_admin) && (
                <button
                  className="btn btn-sm btn-outline-warning"
                  style={{ height: '28px', fontSize: '0.75rem', padding: '2px 8px' }}
                  onClick={() => navigate('/admin/users')}
                >
                  🛠 관리자
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 🔍 검색창 + 정렬 + 글쓰기 */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div className="input-group w-50">
          <input
            type="text"
            className="form-control"
            placeholder="게시글 검색..."
            value={keyword}
            onChange={handleSearchChange}
            onKeyDown={handleKeyDown}
          />
          <button className="btn btn-primary" onClick={handleSearchButtonClick}>
            검색
          </button>
        </div>

        <div className="d-flex align-items-center gap-2">
          <select
            className="form-select"
            style={{ height: '35px', fontSize: '0.875rem' }}
            value={order}
            onChange={handleOrderChange}
          >
            <option value="newest">📅 최신순</option>
            <option value="oldest">📜 오래된순</option>
            <option value="title">🔤 제목순</option>
          </select>
          <Link
            to="/create"
            className="btn btn-primary px-3 py-1"
            style={{ height: '32px', lineHeight: '20px', whiteSpace: 'nowrap', fontSize: '0.875rem' }}
          >
            ✍️ 글작성
          </Link>
        </div>
      </div>

      {/* 📃 게시글 리스트 */}
      <div className="list-group">
        {posts.map((post) => (
          <Link
            to={`/posts/${post.id}`}
            key={post.id}
            className="list-group-item list-group-item-action"
          >
            <h5 className="mb-1">{post.title}</h5>
            <small className="text-muted">
              {post.nickname} | 작성일: {new Date(post.created_at).toLocaleString('ko-KR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false,
              })}
            </small>
          </Link>
        ))}
      </div>

      {/* ⏩ 페이지네이션 */}
      <div className="d-flex justify-content-center mt-4">
        <nav>
          <ul className="pagination">
            {Array.from({ length: totalPages }, (_, i) => (
              <li key={i + 1} className={`page-item ${currentPage === i + 1 ? 'active' : ''}`}>
                <button className="page-link" onClick={() => handlePageChange(i + 1)}>
                  {i + 1}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default PostList;
