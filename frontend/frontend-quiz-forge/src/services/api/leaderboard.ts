import axios from "./axios";

// /services/api/leaderboard.ts
export const getQuizLeaderboard = async (quizCode: string) => {
  const res = await axios.get(`/leaderboard/leaderboard/${quizCode}`); // quizCode is used as quiz_id
  return res.data;
};


// Get overall leaderboard across all quizzes
export const getOverallLeaderboard = async () => {
  const res = await axios.get("/leaderboard/overall");
  return res.data;
};
