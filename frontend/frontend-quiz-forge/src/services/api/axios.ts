import axios from "axios";

const instance = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: false, // change to true if using secure cookies or auth headers
});

export default instance;
