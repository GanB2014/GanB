import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const PostDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, token } = useAuth();

  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentContent, setCommentContent] = useState('');
  const [commentImage, setCommentImage] = useState(null);
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [editedCommentContent, setEditedCommentContent] = useState('');
  const [editedCommentImage, setEditedCommentImage] = useState(null);
  const [replyStates, setReplyStates] = useState({});
  const [editedReplyContent, setEditedReplyContent] = useState('');
  const [editedReplyImage, setEditedReplyImage] = useState(null);
  const [editingReplyId, setEditingReplyId] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/posts/${id}`)
      .then(res => setPost(res.data))
      .catch(err => console.error('게시글 불러오기 실패:', err));
    fetchComments();
  }, [id]);

  const fetchComments = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/comments/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const sorted = res.data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
      setComments(sorted);
    } catch (err) {
      console.error('댓글 불러오기 실패:', err);
    }
  };

  // ✅ 게시글은 KST로 저장되어 있으므로 그대로 출력
  const formatPostDate = (date) => {
    const d = new Date(date);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
  };

  // ✅ 댓글/대댓글은 UTC로 저장되어 있으므로 KST(+9시간)로 보정
  const formatCommentDate = (date) => {
    const d = new Date(date);
    d.setHours(d.getHours() + 9);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('content', commentContent);
    formData.append('post_id', id);
    if (commentImage) formData.append('file', commentImage);

    try {
      await axios.post('http://localhost:8000/comments/', formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCommentContent('');
      setCommentImage(null);
      fetchComments();
    } catch (err) {
      alert('댓글 작성 실패');
    }
  };

  const handleDelete = async (postId) => {
    if (!window.confirm('게시글을 삭제할까요?')) return;
    try {
      await axios.delete(`http://localhost:8000/posts/${postId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      navigate('/');
    } catch (err) {
      alert('삭제 실패');
    }
  };

  const handleForceDeletePost = async () => {
    if (!window.confirm('⚠️ 관리자 권한으로 이 게시글을 강제로 삭제하시겠습니까?')) return;
    try {
      await axios.delete(`http://localhost:8000/admin/force-delete-post/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      navigate('/');
    } catch (err) {
      alert('게시글 강제 삭제 실패');
    }
  };

  const startEditComment = (comment) => {
    setEditingCommentId(comment.id);
    setEditedCommentContent(comment.content);
    setEditedCommentImage(null);
  };

  const handleCommentUpdate = async (commentId) => {
    const formData = new FormData();
    formData.append('content', editedCommentContent);
    if (editedCommentImage) formData.append('file', editedCommentImage);

    try {
      await axios.patch(`http://localhost:8000/comments/${commentId}`, formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditingCommentId(null);
      fetchComments();
    } catch (err) {
      alert('댓글 수정 실패');
    }
  };

  const handleCommentDelete = async (commentId) => {
    if (!window.confirm('댓글을 삭제할까요?')) return;
    try {
      await axios.delete(`http://localhost:8000/comments/${commentId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchComments();
    } catch (err) {
      alert('댓글 삭제 실패');
    }
  };

  const handleForceDeleteComment = async (commentId) => {
    if (!window.confirm('⚠️ 관리자 권한으로 이 댓글을 강제로 삭제하시겠습니까?')) return;
    try {
      await axios.delete(`http://localhost:8000/admin/force-delete-comment/${commentId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchComments();
    } catch (err) {
      alert('댓글 강제 삭제 실패');
    }
  };

  const toggleReplyInput = (commentId) => {
    setReplyStates(prev => ({ ...prev, [commentId]: !prev[commentId] }));
  };

  const handleReplySubmit = async (e, parentId) => {
    e.preventDefault();
    const content = e.target.elements[`reply-${parentId}`].value;
    const image = e.target.elements[`image-${parentId}`].files[0];
    const formData = new FormData();
    formData.append('content', content);
    formData.append('post_id', id);
    formData.append('parent_id', parentId);
    if (image) formData.append('file', image);

    try {
      await axios.post('http://localhost:8000/comments/', formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchComments();
      toggleReplyInput(parentId);
    } catch (err) {
      alert('대댓글 작성 실패');
    }
  };

  const startEditReply = (reply) => {
    setEditingReplyId(reply.id);
    setEditedReplyContent(reply.content);
    setEditedReplyImage(null);
  };

  const handleReplyUpdate = async (replyId) => {
    const formData = new FormData();
    formData.append('content', editedReplyContent);
    if (editedReplyImage) formData.append('file', editedReplyImage);

    try {
      await axios.patch(`http://localhost:8000/comments/${replyId}`, formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditingReplyId(null);
      fetchComments();
    } catch (err) {
      alert('대댓글 수정 실패');
    }
  };

  const handleReplyDelete = async (replyId) => {
    if (!window.confirm('대댓글을 삭제할까요?')) return;
    try {
      await axios.delete(`http://localhost:8000/comments/reply/${replyId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchComments();
    } catch (err) {
      alert('대댓글 삭제 실패');
    }
  };

  const handleForceDeleteReply = async (replyId) => {
    if (!window.confirm('⚠️ 관리자 권한으로 이 대댓글을 강제로 삭제하시겠습니까?')) return;
    try {
      await axios.delete(`http://localhost:8000/admin/force-delete-reply/${replyId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchComments();
    } catch (err) {
      alert('대댓글 강제 삭제 실패');
    }
  };

  if (!post) return <div className="p-4">로딩 중...</div>;

  return (
    <div className="container mt-4">
      <button onClick={() => navigate('/')} className="btn btn-outline-secondary mb-3">← 게시글 목록으로</button>
      <h2 className="mb-3">{post.title}</h2>
      <div className="text-muted mb-2">
        {post.nickname} | {formatPostDate(post.created_at)}
        {user && (
          <span className="float-end">
            {user.user_id === post.user_id && (
              <>
                <button className="btn btn-sm btn-outline-primary me-2" onClick={() => navigate(`/edit/${post.id}`)}>✏️ 수정</button>
                <button className="btn btn-sm btn-outline-danger me-2" onClick={() => handleDelete(post.id)}>🗑 삭제</button>
              </>
            )}
            {!!user.is_admin && (
              <button className="btn btn-sm btn-outline-warning" onClick={handleForceDeletePost}>🛠 삭제</button>
            )}
          </span>
        )}
      </div>
      <hr />

      {post.image_url && (
        <img src={`http://localhost:8000${post.image_url}`} alt="post" className="mb-3" style={{ width: '100%', maxWidth: '850px' }} />
      )}
      <p>{post.content}</p>
      <hr />

      {/* 댓글 리스트 */}
      <ul className="list-group">
        {comments.map(comment => (
          <li key={comment.id} className="list-group-item">
            <div className="d-flex justify-content-between align-items-center mb-1">
              <div>
                <strong>{comment.nickname}</strong> | <span className="text-muted small">{formatCommentDate(comment.created_at)}</span>
              </div>
              {user && (
                <div>
                  {user.id === comment.user_id && (
                    <>
                      <button className="btn btn-sm btn-outline-primary me-1" onClick={() => startEditComment(comment)}>수정</button>
                      <button className="btn btn-sm btn-outline-danger me-1" onClick={() => handleCommentDelete(comment.id)}>삭제</button>
                    </>
                  )}
                  {!!user.is_admin && (
                    <button className="btn btn-sm btn-outline-warning" onClick={() => handleForceDeleteComment(comment.id)}>🛠 삭제</button>
                  )}
                </div>
              )}
            </div>

            {comment.image_url && (
              <img src={`http://localhost:8000${comment.image_url}`} style={{ maxWidth: '150px', maxHeight: '150px' }} alt="comment" className="mb-2" />
            )}

            {editingCommentId === comment.id ? (
              <>
                <textarea className="form-control mb-2" value={editedCommentContent} onChange={(e) => setEditedCommentContent(e.target.value)} />
                <input type="file" className="form-control mb-2" onChange={(e) => setEditedCommentImage(e.target.files[0])} />
                <button className="btn btn-sm btn-success me-2" onClick={() => handleCommentUpdate(comment.id)}>저장</button>
                <button className="btn btn-sm btn-secondary" onClick={() => setEditingCommentId(null)}>취소</button>
              </>
            ) : (
              <>
                <p>{comment.content}</p>
                <button className="btn btn-sm btn-outline-secondary" onClick={() => toggleReplyInput(comment.id)}>↪ 대댓글</button>
              </>
            )}

            {replyStates[comment.id] && (
              <form onSubmit={(e) => handleReplySubmit(e, comment.id)} className="mt-2">
                <textarea name={`reply-${comment.id}`} className="form-control mb-1" required />
                <input type="file" name={`image-${comment.id}`} className="form-control mb-2" accept="image/*" />
                <button type="submit" className="btn btn-sm btn-primary">대댓글 작성</button>
              </form>
            )}

            {comment.replies?.length > 0 && (
              <ul className="mt-2 ps-3">
                {comment.replies.map((reply, index) => (
                  <React.Fragment key={reply.id}>
                    {index === 0 && <hr className="my-2" />} {/* 댓글과 대댓글 사이 구분선 */}
                    {index > 0 && <hr className="my-2" />}     {/* 대댓글 사이 구분선 */}
                    <li className="small mb-2">
                      <div className="d-flex justify-content-between">
                        <div>
                          <strong>{reply.nickname}</strong> | <span className="text-muted">{formatCommentDate(reply.created_at)}</span>
                        </div>
                        {user && (
                          <div>
                            {user.id === reply.user_id && (
                              <>
                                <button className="btn btn-sm btn-outline-primary me-2" onClick={() => startEditReply(reply)}>수정</button>
                                <button className="btn btn-sm btn-outline-danger me-2" onClick={() => handleReplyDelete(reply.id)}>삭제</button>
                              </>
                            )}
                            {!!user.is_admin && (
                              <button className="btn btn-sm btn-outline-warning" onClick={() => handleForceDeleteReply(reply.id)}>🛠 삭제</button>
                            )}
                          </div>
                        )}
                      </div>
                      {reply.image_url && (
                        <div>
                          <img src={`http://localhost:8000${reply.image_url}`} style={{ maxWidth: '150px', maxHeight: '150px' }} alt="reply" className="mb-1" />
                        </div>
                      )}
                      {editingReplyId === reply.id ? (
                        <>
                          <textarea className="form-control mb-1" value={editedReplyContent} onChange={(e) => setEditedReplyContent(e.target.value)} />
                          <input type="file" className="form-control mb-1" onChange={(e) => setEditedReplyImage(e.target.files[0])} />
                          <button className="btn btn-sm btn-success me-2" onClick={() => handleReplyUpdate(reply.id)}>저장</button>
                          <button className="btn btn-sm btn-secondary" onClick={() => setEditingReplyId(null)}>취소</button>
                        </>
                      ) : (
                        <p className="mb-1">{reply.content}</p>
                      )}
                    </li>
                  </React.Fragment>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>

      {/* 댓글 작성 폼 */}
      <form onSubmit={handleCommentSubmit} className="mt-4 mb-5">
        <textarea className="form-control mb-2" placeholder="댓글을 입력하세요" value={commentContent} onChange={(e) => setCommentContent(e.target.value)} required />
        <input type="file" className="form-control mb-2" accept="image/*" onChange={(e) => setCommentImage(e.target.files[0])} />
        <button type="submit" className="btn btn-primary">댓글 작성</button>
      </form>
    </div>
  );
};

export default PostDetail;
