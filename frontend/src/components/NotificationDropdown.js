import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Dropdown } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const NotificationDropdown = ({ buttonStyle }) => {
  const { user, token } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const navigate = useNavigate();

  // 🔄 알림 목록 가져오기 함수
  const fetchNotifications = useCallback(async () => {
    try {
      const res = await axios.get('http://localhost:8000/notifications/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      // 안 읽은 알림만 필터링
      setNotifications(res.data.filter((n) => !n.is_read));
    } catch (err) {
      console.error('알림 조회 실패:', err);
    }
  }, [token]);

  useEffect(() => {
    if (user && token) {
      fetchNotifications();
    }
  }, [user, token, fetchNotifications]);

  // ✅ 알림 클릭 시 읽음 처리 후 해당 게시글로 이동
  const handleClick = async (notif) => {
    try {
      await axios.patch(`http://localhost:8000/notifications/read/${notif.id}/`, null, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setNotifications((prev) => prev.filter((n) => n.id !== notif.id));

      if (notif.post_id) {
        navigate(`/posts/${notif.post_id}`);
      }
    } catch (err) {
      console.error('알림 읽음 처리 실패:', err);
    }
  };

  return (
    <Dropdown align="end">
      <Dropdown.Toggle
        variant="outline-dark"
        size="sm"
        id="dropdown-notifications"
        style={buttonStyle}
      >
        🔔 알림 ({notifications.length})
      </Dropdown.Toggle>

      <Dropdown.Menu style={{ maxHeight: '300px', overflowY: 'auto' }}>
        {notifications.length === 0 ? (
          <Dropdown.Item disabled>새 알림이 없습니다.</Dropdown.Item>
        ) : (
          notifications.map((notif) => (
            <Dropdown.Item key={notif.id} onClick={() => handleClick(notif)}>
              {notif.message}
            </Dropdown.Item>
          ))
        )}
        {/* ✅ 항상 표시되는 전체 보기 버튼 */}
        <Dropdown.Divider />
        <Dropdown.Item
          onClick={() => navigate('/notifications')}
          className="text-center"
          style={{
            fontWeight: 'bold',
            paddingTop: '4px',
            paddingBottom: '4px',
            fontSize: '0.85rem'
          }}
        >
         전체 보기
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default NotificationDropdown;
