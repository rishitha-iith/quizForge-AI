import { BrowserRouter as Router, useLocation } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "@/components/common/Navbar";
import { useEffect } from "react";

// Wrapper to use hooks outside Router
function AppWrapper() {
  const location = useLocation();

  // Define paths where Navbar should be hidden
  const hideNavbarRoutes = ["/login", "/signup","/"];
  const shouldHideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (
    <>
      {!shouldHideNavbar && <Navbar />}
      <AppRoutes />
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppWrapper />
      </Router>
    </AuthProvider>
  );
}

export default App;
