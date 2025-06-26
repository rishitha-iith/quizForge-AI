import { Routes, Route } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import SignupPage from "../pages/SignupPage";
import Home from "../pages/Home";
import ExplanationPage from "../pages/ExplanationPage";
import LeaderboardPage from "../pages/LeaderboardPage";
import ProtectedRoute from "../components/common/ProtectedRoute";
import UploadForm from "@/components/UploadForm";
import StartQuiz from "@/components/StartQuiz";
import JoinQuiz from "@/components/JoinQuiz";
import QuizPage from "@/components/QuizPage";
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/join" element={<ProtectedRoute><JoinQuiz /></ProtectedRoute>} />
      <Route path="/upload" element={<ProtectedRoute><UploadForm /></ProtectedRoute>} />
      <Route
        path="/start-quiz/:quiz_id"
        element={<ProtectedRoute><StartQuiz /></ProtectedRoute>}
      />
      <Route path="/quiz/:quizCode" element={<ProtectedRoute><QuizPage /></ProtectedRoute>} />
      <Route path="/explanations/:quizName/:userId" element={<ProtectedRoute><ExplanationPage /></ProtectedRoute>} />
      <Route path="/leaderboard/:quizCode" element={<ProtectedRoute><LeaderboardPage /></ProtectedRoute>} />
    </Routes>
  );
}
