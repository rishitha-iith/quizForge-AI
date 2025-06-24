import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getQuizQuestions } from "@/services/api/getQuiz";
import { submitAnswers } from "@/services/api/quiz";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";

type Question = {
  question_id: number;
  question: string;
  options: string[];
};

export default function QuizRoom() {
  const { quizCode } = useParams<{ quizCode: string }>();
  const { userId } = useAuth();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [timeLeft, setTimeLeft] = useState<number>(0); // in seconds
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Fetch questions on mount
  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const data = await getQuizQuestions(quizCode!, userId!);
        setQuestions(data.questions);
        setTimeLeft(data.duration_minutes * 60); // convert to seconds
      } catch (err) {
        toast.error("Failed to load quiz");
        navigate("/home");
      }
    };
    fetchQuiz();
  }, [quizCode, userId, navigate]);

  // Countdown Timer
  useEffect(() => {
    if (timeLeft <= 0) {
      handleSubmit(); // Auto-submit
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const handleOptionSelect = (option: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questions[currentIndex].question_id]: option,
    }));
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await submitAnswers({
        quiz_code: quizCode!,
        user_id: userId!,
        answers: Object.entries(answers).map(([id, answer]) => ({
          question_id: Number(id),
          answer,
        })),
      });
      toast.success("Answers submitted!");
      navigate(`/explanations/${quizCode}`);
    } catch (err) {
      toast.error("Submission failed");
    } finally {
      setIsSubmitting(false);
    }
  };

  const current = questions[currentIndex];
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 p-6">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold text-blue-800">Quiz Room</h1>
          <div className="text-right">
            <span className="text-sm font-semibold text-red-600">
              Time Left: {minutes}:{seconds.toString().padStart(2, "0")}
            </span>
            <Progress value={(timeLeft / (questions.length * 60)) * 100} className="h-2 mt-1" />
          </div>
        </div>

        {current && (
          <Card className="shadow-md border border-blue-200">
            <CardContent className="p-6 space-y-4">
              <h2 className="text-lg font-semibold text-gray-800">
                Q{currentIndex + 1}. {current.question}
              </h2>
              <div className="space-y-3">
                {current.options.map((opt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleOptionSelect(opt)}
                    className={`w-full text-left px-4 py-2 rounded-lg border transition-all
                      ${answers[current.question_id] === opt
                        ? "bg-blue-100 border-blue-500 text-blue-700 font-medium"
                        : "bg-white hover:bg-gray-100 border-gray-300"}
                    `}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        <div className="flex justify-between pt-4">
          <Button
            variant="outline"
            disabled={currentIndex === 0}
            onClick={() => setCurrentIndex((i) => i - 1)}
          >
            Previous
          </Button>
          {currentIndex < questions.length - 1 ? (
            <Button
              onClick={() => setCurrentIndex((i) => i + 1)}
              disabled={!answers[current.question_id]}
            >
              Next
            </Button>
          ) : (
            <Button
              className="bg-green-600 hover:bg-green-700 text-white"
              onClick={handleSubmit}
              disabled={Object.keys(answers).length !== questions.length || isSubmitting}
            >
              {isSubmitting ? "Submitting..." : "Submit Quiz"}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
