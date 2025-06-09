import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function UploadForm() {
  const [pdf, setPdf] = useState<File | null>(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [numUsers, setNumUsers] = useState(1);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pdf) return;

    const formData = new FormData();
    formData.append('pdf_file', pdf);
    formData.append('num_questions', numQuestions.toString());
    formData.append('num_users_input', numUsers.toString());

    const response = await axios.post('https://quizforge-ai-3.onrender.com/generate_quiz', formData);
    const quiz = response.data;

    // Store quiz in localStorage for now
    localStorage.setItem('quiz', JSON.stringify(quiz));

    // Start user quiz
    const userId = `user-${Date.now()}`;
    await axios.post(`https://quizforge-ai-3.onrender.com/start_user_quiz/${userId}`, quiz);

    navigate(`/quiz/${userId}`);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input type="file" accept="application/pdf" onChange={(e) => setPdf(e.target.files?.[0] || null)} />
      <input
        type="number"
        min={1}
        value={numQuestions}
        onChange={(e) => setNumQuestions(+e.target.value)}
        className="border p-2 w-full"
        placeholder="Number of Questions"
      />
      <input
        type="number"
        min={1}
        value={numUsers}
        onChange={(e) => setNumUsers(+e.target.value)}
        className="border p-2 w-full"
        placeholder="Number of Users"
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        Generate Quiz
      </button>
    </form>
  );
}
