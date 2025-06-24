import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import type { ReactNode } from "react"; // ✅ Add this line

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { userId } = useAuth();

  if (!userId) {
    return <Navigate to="/" />;
  }

  return <>{children}</>; // ✅ Wrap in fragment if using ReactNode
};

export default ProtectedRoute;
