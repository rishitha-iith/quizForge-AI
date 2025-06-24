import axios from "./axios";

export const getExplanations = async (quizCode: string, userId: string) => {
  const res = await axios.get(`/explanations/${quizCode}/${userId}`);
  return res.data;
};
