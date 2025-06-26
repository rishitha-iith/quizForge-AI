import axios from "./axios";

export const generateQuiz = async (formData: FormData) => {
  const res = await axios.post("/quiz/generate_quiz", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};


export const submitAnswers = async (payload: {
  token: string;
  quiz_id: string;
  answers: Record<number, string | null>;
  time_taken: number;
}) => {
  const formData = new FormData();
  formData.append("token", payload.token);
  formData.append("quiz_id", payload.quiz_id);
  formData.append("answers", JSON.stringify(payload.answers)); // this will now be clean JSON
  formData.append("time_taken", payload.time_taken.toString());

  const res = await axios.post("/results/submit_answers", formData); // no need to set Content-Type
  return res.data;
};
