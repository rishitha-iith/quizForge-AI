import React from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Login from "./components/auth/Login";
import Signup from "./components/auth/Signup";
import UploadForm from "./components/UploadForm";
import QuizPage from "./components/QuizPage";
import Leaderboard from "./components/Leaderboard";
import { getUserId } from "./utils/auth";

function Home() {
  const [step, setStep] = React.useState<"upload" | "quiz" | "leaderboard">("upload");
  const [userId, setUserId] = React.useState(getUserId() || "");

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      {step === "upload" && (
        <UploadForm
          onGenerated={() => {
            setStep("quiz");
          }}
        />
      )}
      {step === "quiz" && (
        <QuizPage userId={userId} onSubmitted={() => setStep("leaderboard")} />
      )}
      {step === "leaderboard" && <Leaderboard />}
    </div>
  );
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const userId = getUserId();
  return userId ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}
