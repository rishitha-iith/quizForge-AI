import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const loginUser = async (email: string, password: string) => {
  const res = await axios.post(`${API_BASE}/login`, { email, password });
  return res.data;
};

// src/services/api.ts

export const signupUser = async ({
  username,
  email,
  password,
}: {
  username: string;
  email: string;
  password: string;
}) => {
  const response = await fetch(`${API_BASE}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // ✅ Send as JSON
    },
    body: JSON.stringify({
      username,
      email,
      password,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    console.error("Signup error:", errorData);
    throw new Error("Signup failed");
  }

  return await response.json(); // Should return: { user_id: string }
};



export const generateQuiz = async (formData: FormData) => {
  const res = await axios.post(`${API_BASE}/generate_quiz`, formData);
  return res.data;
};

export const getQuiz = async () => {
  const res = await axios.get(`${API_BASE}/get_quiz`);
  return res.data;
};

export const submitAnswers = async (answers: any) => {
  const res = await axios.post(`${API_BASE}/submit_answers`, answers);
  return res.data;
};

export const getLeaderboard = async () => {
  const res = await axios.get(`${API_BASE}/leaderboard`);
  return res.data;
};
