import React, { useEffect, useState } from "react";
import axios from "axios";

const Leaderboard = () => {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/leaderboard", {
      headers: {
        "ngrok-skip-browser-warning": "true"
      }
    });
    setData(res.data);
  } catch (err) {
    console.error("Error fetching leaderboard:", err);
  }
};

    fetchData();
  }, []);

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Leaderboard</h2>
      <ul className="space-y-2">
        {data.map((user, index) => (
          <li key={index} className="border p-2 rounded shadow flex justify-between">
            <span>User: {user.user_id}</span>
            <span>Score: {user.score}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;
