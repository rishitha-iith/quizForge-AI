import axios from "./axios";
export const signupUser = async (data: { username: string; email: string; password: string }) => {
  const res = await axios.post("/auth/signup", data);
  return res.data; // should return user_id or token
};



export async function loginUser(identifier: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("identifier", identifier);
  formData.append("password", password);

  const response = await axios.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return response.data; // token, user_id, username
}
