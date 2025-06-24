import axios from "./axios";

export const getOverallLeaderboard = async () => {
  const res = await axios.get("/leaderboard/overall");
  return res.data;
};

export const getQuizLeaderboard = async (quizCode: string) => {
  const res = await axios.get(`/leaderboard/${quizCode}`);
  return res.data;
};
