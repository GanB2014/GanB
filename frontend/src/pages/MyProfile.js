// src/pages/MyProfile.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const MyProfile = () => {
  const { user, login } = useAuth();
  const navigate = useNavigate();

  const [nickname, setNickname] = useState('');
  const [myPosts, setMyPosts] = useState([]);
  const [postPage, setPostPage] = useState(1);
  const [postTotalPages, setPostTotalPages] = useState(1);

  const [myComments, setMyComments] = useState([]);
  const [commentPage, setCommentPage] = useState(1);
  const [commentTotalPages, setCommentTotalPages] = useState(1);

  const pageSize = 8;

  useEffect(() => {
    if (!user) return;
    const token = localStorage.getItem('token');
    setNickname(user.nickname);

    fetchPosts(token, postPage);
    fetchComments(token, commentPage);
  }, [user, postPage, commentPage]);

  const fetchPosts = async (token, page) => {
    try {
      const res = await axios.get(`http://localhost:8000/user/my-posts?page=${page}&page_size=${pageSize}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMyPosts(res.data.posts);
      setPostTotalPages(res.data.total_pages);
    } catch (err) {
      console.error('게시글 로딩 실패:', err);
    }
  };

  const fetchComments = async (token, page) => {
    try {
      const res = await axios.get(`http://localhost:8000/user/my-comments?page=${page}&page_size=${pageSize}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMyComments(res.data.comments);
      setCommentTotalPages(res.data.total_pages);
    } catch (err) {
      console.error('댓글 로딩 실패:', err);
    }
  };

  const handleNicknameChange = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.patch(
        'http://localhost:8000/user/nickname',
        { nickname },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (res.data.access_token) {
        login(res.data.access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`;
      }
      alert('닉네임이 성공적으로 변경되었습니다.');
    } catch (err) {
      alert('닉네임 변경 실패');
      console.error(err);
    }
  };

  const renderPagination = (currentPage, totalPages, setPageFn) => (
    <nav>
      <ul className="pagination justify-content-center mt-2">
        {Array.from({ length: totalPages }, (_, i) => (
          <li key={i + 1} className={`page-item ${currentPage === i + 1 ? 'active' : ''}`}>
            <button className="page-link" onClick={() => setPageFn(i + 1)}>
              {i + 1}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );

  return (
    <div className="container mt-4">
      <button onClick={() => navigate('/')} className="btn btn-outline-secondary mb-3">
        ← 게시글 목록으로
      </button>

      <h2 className="text-center fs-1 mb-5">내 프로필</h2>

      <div className="row">
        <div className="col-md-4">
          <div className="card p-3 mb-3">
            <h5>닉네임 변경</h5>
            <input
              type="text"
              className="form-control mb-2"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
            />
            <button className="btn btn-primary" onClick={handleNicknameChange}>
              변경하기
            </button>
          </div>
        </div>

        <div className="col-md-8">
          <div className="mb-4">
            <h5>📌 내가 쓴 게시글</h5>
            <ul className="list-group">
              {myPosts.map((post) => (
                <li key={post.id} className="list-group-item">
                  <strong>{post.title}</strong>
                </li>
              ))}
            </ul>
            {renderPagination(postPage, postTotalPages, setPostPage)}
          </div>

          <div>
            <h5>💬 내가 쓴 댓글</h5>
            <ul className="list-group">
              {myComments.map((comment) => (
                <li key={comment.id} className="list-group-item">
                  {comment.content}
                </li>
              ))}
            </ul>
            {renderPagination(commentPage, commentTotalPages, setCommentPage)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyProfile;
