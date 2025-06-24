import axios from "./axios";

export const getQuizQuestions = async (quizCode: string, userId: string) => {
  const res = await axios.get(`/get_quiz/${quizCode}/${userId}`);
  return res.data;
};
