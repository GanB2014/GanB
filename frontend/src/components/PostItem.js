import React from 'react';

const PostItem = ({ post }) => {
  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
      <h2>{post.title}</h2>
      <p>{post.content}</p>
      {post.image_url && (
        <img
          src={`http://localhost:8000${post.image_url}`}
          alt={post.title}
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      )}
      <small>{new Date(post.created_at).toLocaleString()}</small>
    </div>
  );
};

export default PostItem;
