import React from "react";
import axios from "axios";

function StartQuiz({ userId, quiz, onStarted }: { userId: string, quiz: any, onStarted: (questions: any[]) => void }) {
  const handleStart = async () => {
    try {
      await axios.post(
  `http://127.0.0.1:8000/start_user_quiz/${userId}`,
  quiz,
  {
    headers: {
      "ngrok-skip-browser-warning": "true"
    }
  }
);

const res = await axios.get(
  `http://127.0.0.1:8000/get_user_quiz/${userId}`,
  {
    headers: {
      "ngrok-skip-browser-warning": "true"
    }
  }
);

      onStarted(res.data);  // Move to quiz page
    } catch (err) {
      console.error("Start quiz error", err);
    }
  };

  return <button onClick={handleStart} className="bg-blue-500 text-white px-4 py-2 rounded">Start Quiz</button>;
}

export default StartQuiz;
