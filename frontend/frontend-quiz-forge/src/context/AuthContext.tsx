import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

type AuthContextType = {
  userId: string | null;
  setUserId: (id: string) => void;
  token: string | null;
  setToken: (token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [userId, setUserIdState] = useState<string | null>(
    localStorage.getItem("userId")
  );

  const [token, setTokenState] = useState<string | null>(
    localStorage.getItem("token")
  );

  const setUserId = (id: string) => {
    setUserIdState(id);
    localStorage.setItem("userId", id);
  };

  const setToken = (newToken: string) => {
    setTokenState(newToken);
    localStorage.setItem("token", newToken);
  };

  const logout = () => {
    setUserIdState(null);
    setTokenState(null);
    localStorage.removeItem("userId");
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ userId, setUserId, token, setToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
};
