import React, { useState } from "react";
import axios from "axios";
import { getUserId } from "../utils/auth";

export default function UploadForm({ onGenerated }: { onGenerated: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [numUsers, setNumUsers] = useState(1);

  const userId = getUserId(); // ✅ get userId from localStorage

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !userId) {
      alert("Missing file or user ID");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("num_questions", numQuestions.toString());
    formData.append("num_users", numUsers.toString());
    formData.append("user_id", userId);

    try {
      await axios.post("http://127.0.0.1:8000/generate_quiz", formData);
      onGenerated();
    } catch (err) {
      alert("Quiz generation failed!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <input
        type="number"
        placeholder="Number of Questions"
        value={numQuestions}
        onChange={(e) => setNumQuestions(Number(e.target.value))}
        className="w-full border p-2 rounded"
      />
      <input
        type="number"
        placeholder="Number of Users"
        value={numUsers}
        onChange={(e) => setNumUsers(Number(e.target.value))}
        className="w-full border p-2 rounded"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Generate Quiz
      </button>
    </form>
  );
}
