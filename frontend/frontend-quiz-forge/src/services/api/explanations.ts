// src/services/api/explanations.ts
import axios from "./axios";

export const getExplanations = async (quizName: string, userId: string) => {
  console.log("Fetching explanations for quiz:", quizName, "and user:", userId);
  const res = await axios.get(`/explanations/explanations/${quizName}/${userId}`);
  return res.data;
};
