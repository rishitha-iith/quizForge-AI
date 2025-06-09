import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function ResultPage() {
  const { userId } = useParams();
  const [leaderboard, setLeaderboard] = useState<any[]>([]);

  useEffect(() => {
    axios.get('https://quizforge-ai-3.onrender.com/leaderboard').then((res) => {
      setLeaderboard(res.data);
    });
  }, []);

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Leaderboard</h2>
      <table className="w-full table-auto border">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-2 border">User ID</th>
            <th className="p-2 border">Score</th>
            <th className="p-2 border">Time Taken</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry, i) => (
            <tr key={i} className={entry.user_id === userId ? 'bg-green-100' : ''}>
              <td className="p-2 border">{entry.user_id}</td>
              <td className="p-2 border">{entry.score}</td>
              <td className="p-2 border">{entry.time_taken}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
