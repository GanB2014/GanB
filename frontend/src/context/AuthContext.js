import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUserState] = useState(null);
  const [token, setToken] = useState(null);

  // ✅ 토큰 저장 시 관리자 여부 포함
  const login = (newToken) => {
    const decoded = jwtDecode(newToken);
    const updatedUser = {
      id: decoded.id,
      user_id: decoded.sub,
      nickname: decoded.nickname,
      is_admin: decoded.is_admin, // ✅ 관리자 여부 포함
    };
    setUserState(updatedUser);
    setToken(newToken);
    localStorage.setItem("token", newToken);
  };

  const logout = () => {
    setUserState(null);
    setToken(null);
    localStorage.removeItem("token");
  };

  // ✅ 앱 시작 시 토큰 복원 + 관리자 여부 포함
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      try {
        const decoded = jwtDecode(savedToken);
        const restoredUser = {
          id: decoded.id,
          user_id: decoded.sub,
          nickname: decoded.nickname,
          is_admin: decoded.is_admin, // ✅ 관리자 여부 포함
        };
        setUserState(restoredUser);
        setToken(savedToken);
      } catch (e) {
        localStorage.removeItem("token");
      }
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
