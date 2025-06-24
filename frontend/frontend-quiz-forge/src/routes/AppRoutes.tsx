import { Routes, Route } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import SignupPage from "../pages/SignupPage";
import Home from "../pages/Home";
import QuizRoom from "../pages/QuizRoom";
import ExplanationPage from "../pages/ExplanationPage";
import LeaderboardPage from "../pages/LeaderboardPage";
import ProtectedRoute from "../components/common/ProtectedRoute";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/quiz/:quizCode" element={<ProtectedRoute><QuizRoom /></ProtectedRoute>} />
      <Route path="/explanations/:quizCode" element={<ProtectedRoute><ExplanationPage /></ProtectedRoute>} />
      <Route path="/leaderboard/:quizCode" element={<ProtectedRoute><LeaderboardPage /></ProtectedRoute>} />
    </Routes>
  );
}
