import axios from "./axios";

// Get badges earned by a user
export const getUserBadges = async (userId: string) => {
  const res = await axios.get(`/badges/badges/${userId}`);
  return res.data;
};
