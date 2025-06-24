import axios from "./axios";

export const getUserBadges = async (userId: string) => {
  const res = await axios.get(`/badges/${userId}`);
  return res.data;
};
