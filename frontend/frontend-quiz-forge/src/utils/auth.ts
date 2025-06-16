export const setUserId = (userId: string) => {
  localStorage.setItem("userId", userId);
};

export const getUserId = () => {
  return localStorage.getItem("userId");
};

export const logout = () => {
  localStorage.removeItem("userId");
};
