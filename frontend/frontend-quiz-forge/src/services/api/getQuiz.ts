import axios from "./axios";

export const getQuizQuestions = async (quizCode: string, userId: string) => {
  const response = await axios.get(`/get_quiz/${quizCode}/${userId}`);
  console.log("get quiz data",response.data);
  return response.data;
};
