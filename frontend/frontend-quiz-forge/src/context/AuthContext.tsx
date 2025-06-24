import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

type AuthContextType = {
  userId: string | null;
  setUserId: (id: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [userId, setUserIdState] = useState<string | null>(
    localStorage.getItem("userId")
  );

  const setUserId = (id: string) => {
    setUserIdState(id);
    localStorage.setItem("userId", id);
  };

  const logout = () => {
    setUserIdState(null);
    localStorage.removeItem("userId");
  };

  return (
    <AuthContext.Provider value={{ userId, setUserId, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
};
