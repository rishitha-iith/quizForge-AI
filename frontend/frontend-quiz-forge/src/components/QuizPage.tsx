import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { submitAnswers } from "@/services/api/quiz";
import { getQuizQuestions } from "@/services/api/getQuiz";

interface Question {
  question_id: number;
  question: string;
  options: string[];
}

const QuizPage = () => {
  const { quizCode } = useParams();
  const userId = localStorage.getItem("user_id") || "";
  const quizName = localStorage.getItem("quiz_name") || "";
  const navigate = useNavigate();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [quizId, setQuizId] = useState<string>("");
  const [submitted, setSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch quiz data
  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        setIsLoading(true);
        const data = await getQuizQuestions(quizCode!, userId);
        console.log("Loaded quiz data:", data);

        setQuestions(data.questions || []);
        setQuizId(data.quiz_id || "");
        if (data.quiz_name) {
          localStorage.setItem("quiz_name", data.quiz_name);
        }
        setError(null);
      } catch (err: any) {
        console.error("Quiz fetch error:", err);
        setError(err?.response?.data?.detail || "Failed to load quiz.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuiz();
  }, [quizCode, userId]);

  // Handle answer selection
  const handleAnswerChange = (qid: number, option: string) => {
    setAnswers((prev) => ({ ...prev, [qid]: option }));
  };

  // Handle quiz submission
  const handleSubmit = async () => {
    if (submitted) return;
    try {
      setIsLoading(true);
      const payload = {
        token: localStorage.getItem("token") || "",
        quiz_id: quizId,
        answers: JSON.stringify(answers), // Send as stringified JSON
        time_taken: 0, // You can implement timing later
      };

      const response = await submitAnswers(payload);
      console.log("Submit response:", response);

      setSubmitted(true);
      navigate(`/explanations/${quizName}/${userId}`);
    } catch (err) {
      console.error("Submission error:", err);
      setError("Failed to submit answers. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && questions.length === 0) {
    return <div className="p-4 text-center">Loading quiz...</div>;
  }

  if (error) {
    return <div className="p-4 text-center text-red-600">{error}</div>;
  }

  return (
    <div className="p-4 space-y-6 max-w-2xl mx-auto">
      <div className="flex justify-end">
        <button
          onClick={handleSubmit}
          className="bg-green-600 text-white px-4 py-1 rounded text-sm"
          disabled={submitted || isLoading}
        >
          {isLoading ? "Submitting..." : submitted ? "Submitted" : "Submit Quiz"}
        </button>
      </div>

      {questions.map((q, idx) => (
        <div key={q.question_id} className="border p-4 rounded shadow">
          <p className="font-semibold">
            {idx + 1}. {q.question}
          </p>
          {q.options.map((opt, i) => {
            const letter = String.fromCharCode(65 + i); // A, B, C, D
            return (
              <label key={i} className="block mt-2">
                <input
                  type="radio"
                  name={`q${q.question_id}`}
                  value={letter}
                  checked={answers[q.question_id] === letter}
                  onChange={() => handleAnswerChange(q.question_id, letter)}
                  disabled={submitted}
                  className="mr-2"
                />
                {letter}. {opt}
              </label>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default QuizPage;
