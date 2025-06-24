import axios from "./axios";

export const getResult = async (quizCode: string, userId: string) => {
  const res = await axios.get(`/results/${quizCode}/${userId}`);
  return res.data;
};
