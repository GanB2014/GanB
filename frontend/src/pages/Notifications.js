import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Notifications = () => {
  const { user, token } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await axios.get('http://localhost:8000/notifications/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setNotifications(res.data);
      } catch (err) {
        console.error('알림 전체 조회 실패:', err);
      }
    };

    if (user && token) {
      fetchNotifications();
    }
  }, [user, token]);

  const handleClick = async (notif) => {
    try {
      await axios.patch(`http://localhost:8000/notifications/read/${notif.id}/`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });
      navigate(`/posts/${notif.post_id}`);
    } catch (err) {
      console.error('알림 읽음 처리 실패:', err);
    }
  };

  return (
    <div className="container mt-4">
      <h3>🔔 전체 알림</h3>
      <ul className="list-group mt-3">
        {notifications.length === 0 ? (
          <li className="list-group-item text-muted">알림이 없습니다.</li>
        ) : (
          notifications.map(notif => (
            <li
              key={notif.id}
              className={`list-group-item d-flex justify-content-between align-items-center ${notif.is_read ? '' : 'fw-bold'}`}
              style={{ cursor: 'pointer' }}
              onClick={() => handleClick(notif)}
            >
              {notif.message}
              <span className="badge bg-secondary">{new Date(notif.created_at).toLocaleString()}</span>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default Notifications;
