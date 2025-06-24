import axios from "./axios";

export const generateQuiz = async (formData: FormData) => {
  const res = await axios.post("/quiz/generate_quiz", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const submitAnswers = async (data: {
  quiz_code: string;
  user_id: string;
  answers: { question_id: number; answer: string }[];
}) => {
  const res = await axios.post("/quiz/submit_answers", data);
  return res.data;
};
