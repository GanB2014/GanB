import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const EditPost = () => {
  const { id } = useParams(); // 게시글 ID
  const { token } = useAuth(); // 로그인 토큰
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    title: '',
    content: '',
    image: null,
    image_url: '',
  });

  const [loading, setLoading] = useState(true);

  // 게시글 데이터 불러오기
  useEffect(() => {
    axios.get(`http://localhost:8000/posts/${id}`)
      .then(res => {
        setFormData({
          title: res.data.title ?? '',
          content: res.data.content ?? '',
          image: null,
          image_url: res.data.image_url || '',
        });
        setLoading(false);
      })
      .catch(err => {
        console.error('게시글 불러오기 실패', err);
        alert('게시글을 불러오지 못했습니다.');
        navigate('/');
      });
  }, [id, navigate]);

  // 입력 변경 처리
  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: files ? files[0] : value
    }));
  };

  // 제출 처리
  const handleSubmit = async (e) => {
    e.preventDefault();
    const updateData = new FormData();
    updateData.append('title', formData.title);
    updateData.append('content', formData.content);
    if (formData.image) {
      updateData.append('file', formData.image);
    }

    try {
      await axios.patch(`http://localhost:8000/posts/${id}`, updateData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        }
      });
      alert('게시글이 수정되었습니다.');
      navigate(`/posts/${id}`);
    } catch (err) {
      console.error('게시글 수정 실패', err);
      alert('게시글 수정에 실패했습니다.');
    }
  };

  if (loading) return <div className="p-4">로딩 중...</div>;

  return (
    <div className="container mt-4">
      <h2>🛠 게시글 수정</h2>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div className="mb-3">
          <label className="form-label">제목</label>
          <input
            type="text"
            name="title"
            className="form-control"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">내용</label>
          <textarea
            name="content"
            className="form-control"
            rows="5"
            value={formData.content ?? ''}
            onChange={handleChange}
            required
          />
        </div>

        {formData.image_url && (
          <div className="mb-3">
            <img
              src={`http://localhost:8000${formData.image_url}`}
              alt="기존 이미지"
              width="300"
              className="mb-2 d-block"
            />
          </div>
        )}

        <div className="mb-3">
          <label className="form-label">새 이미지 선택 (선택)</label>
          <input
            type="file"
            name="image"
            className="form-control"
            accept="image/*"
            onChange={handleChange}
          />
        </div>

        <button type="submit" className="btn btn-success">수정 완료</button>
      </form>
    </div>
  );
};

export default EditPost;
