import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { getQuizQuestions } from "@/services/api/getQuiz";
import { useAuth } from "@/context/AuthContext";

const JoinQuiz = () => {
  const [quizCode, setQuizCode] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { userId } = useAuth();

  const handleJoin = async () => {
    if (!quizCode.trim()) {
      toast.error("Please enter a quiz code.");
      return;
    }

    if (!userId) {
      toast.error("You must be logged in to join a quiz.");
      return;
    }

    setLoading(true);
    try {
      // Attempt to fetch quiz questions (which will fail if code is invalid or user already attempted)
      await getQuizQuestions(quizCode, userId);

      toast.success("Quiz found! Redirecting...");
      navigate(`/quiz/${quizCode}`);
    } catch (error: any) {
      toast.error(
        error.response?.data?.detail || "Invalid quiz code or access denied."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-zinc-900 dark:to-zinc-800">
      <div className="bg-white dark:bg-zinc-900 p-10 rounded-2xl shadow-lg w-full max-w-md">
        <h2 className="text-3xl font-bold text-center mb-6 text-indigo-600 dark:text-white">
          Join a Quiz
        </h2>

        <Input
          type="text"
          placeholder="Enter Quiz Code"
          value={quizCode}
          onChange={(e) => setQuizCode(e.target.value)}
          className="mb-4"
        />

        <Button
          onClick={handleJoin}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700"
        >
          {loading ? "Joining..." : "Join Quiz"}
        </Button>
      </div>
    </div>
  );
};

export default JoinQuiz;
