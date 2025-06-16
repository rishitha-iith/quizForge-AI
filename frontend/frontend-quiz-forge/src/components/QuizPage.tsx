import React, { useEffect, useState } from "react";
import axios from "axios";

const QuizPage = ({ userId, onSubmitted }: { userId: string, onSubmitted: () => void }) => {
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});

  useEffect(() => {
    const fetchQuiz = async () => {
      const res = await axios.get(`http://127.0.0.1:8000/get_quiz`, {
        params: { user_id: userId }
      });
      setQuestions(res.data);
    };
    fetchQuiz();
  }, [userId]);

  const handleChange = (index: number, selected: string) => {
    setAnswers(prev => ({ ...prev, [index]: selected }));
  };

 const handleSubmit = async () => {
  const form = new FormData();
  form.append("user_id", userId);
  form.append("answers", JSON.stringify(answers));

  try {
    await axios.post("http://127.0.0.1:8000/submit_answers", form, {
      headers: {
        "ngrok-skip-browser-warning": "true"
      }
    });
    onSubmitted();
  } catch (err) {
    console.error("Error submitting answers:", err);
  }
};


  return (
    <div className="p-4 space-y-4 max-w-2xl mx-auto">
      {questions.map((q, idx) => (
        <div key={idx} className="border p-4 rounded shadow">
          <p className="font-semibold">{idx + 1}. {q.question}</p>
          {q.options.map((opt: string, i: number) => {
            const letter = String.fromCharCode(65 + i);
            return (
              <label key={i} className="block">
                <input
                  type="radio"
                  name={`q${idx}`}
                  value={letter}
                  checked={answers[idx] === letter}
                  onChange={() => handleChange(idx, letter)}
                />
                <span className="ml-2">{letter}. {opt}</span>
              </label>
            );
          })}
        </div>
      ))}
      <button onClick={handleSubmit} className="bg-green-600 text-white px-6 py-2 rounded">
        Submit Answers
      </button>
    </div>
  );
};

export default QuizPage;
