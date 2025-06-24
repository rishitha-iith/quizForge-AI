import { useLocation, useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import { Copy } from "lucide-react";

export default function StartQuiz() {
  const { quiz_id } = useParams<{ quiz_id: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const state = location.state as {
    quiz_name: string;
    difficulty: string;
    duration_minutes: number;
    num_users: number;
  };

  if (!state) {
    toast.error("Quiz details not found. Redirecting to upload...");
    navigate("/upload");
    return null;
  }

  const { quiz_name, difficulty, duration_minutes, num_users } = state;

  const handleStart = () => {
    navigate(`/quiz/${quiz_id}`);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(quiz_id || "");
    toast.success("Quiz Code copied to clipboard!");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <motion.div
        className="w-full max-w-md"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="shadow-lg border border-blue-200">
          <CardContent className="p-6">
            <h2 className="text-2xl font-bold mb-4 text-center text-blue-700">
              Quiz Summary
            </h2>
            <div className="space-y-3 text-blue-900">
              <div>
                <span className="font-semibold">Quiz Name:</span> {quiz_name}
              </div>
              <div className="flex items-center justify-between gap-2">
                <span>
                  <span className="font-semibold">Quiz Code:</span> {quiz_id}
                </span>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  className="text-sm"
                  onClick={handleCopy}
                >
                  <Copy className="w-4 h-4 mr-1" /> Copy
                </Button>
              </div>
              <div>
                <span className="font-semibold">Difficulty:</span> {difficulty}
              </div>
              <div>
                <span className="font-semibold">Duration:</span>{" "}
                {duration_minutes === 0
                  ? "AI will assign duration"
                  : `${duration_minutes} min`}
              </div>
              <div>
                <span className="font-semibold">Participants:</span> {num_users}
              </div>
            </div>

            <Button
              className="w-full mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white text-lg"
              onClick={handleStart}
            >
              Start Quiz
            </Button>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
