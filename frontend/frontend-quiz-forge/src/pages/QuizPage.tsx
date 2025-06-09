import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import type { Question } from '../types';


export default function QuizPage() {
  const { userId } = useParams();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`https://quizforge-ai-3.onrender.com/get_user_quiz/${userId}`).then((res) => {
      setQuestions(res.data);
    });
  }, [userId]);

  const submitAnswers = async () => {
    await axios.post(`https://quizforge-ai-3.onrender.com/submit_user_answers/${userId}`, answers);
    navigate(`/result/${userId}`);
  };

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h2 className="text-xl font-semibold mb-4">Quiz</h2>
      {questions.map((q, idx) => (
        <div key={idx} className="mb-4">
          <p className="font-medium">{idx + 1}. {q.question}</p>
          <div className="space-y-1">
            {q.options.map((opt, i) => (
              <label key={i} className="block">
                <input
                  type="radio"
                  name={`q${idx}`}
                  value={String.fromCharCode(65 + i)}
                  checked={answers[idx] === String.fromCharCode(65 + i)}
                  onChange={() => setAnswers((prev) => ({ ...prev, [idx]: String.fromCharCode(65 + i) }))}
                />{" "}
                {opt}
              </label>
            ))}
          </div>
        </div>
      ))}
      <button onClick={submitAnswers} className="mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
        Submit
      </button>
    </div>
  );
}
