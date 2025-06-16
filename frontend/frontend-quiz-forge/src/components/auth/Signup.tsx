import React, { useState } from "react";
import { signupUser } from "../../services/api";
import { setUserId } from "../../utils/auth";
import { useNavigate, Link } from "react-router-dom";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await signupUser({ username, email, password });
      setUserId(res.user_id);
      navigate("/home");
    } catch (err) {
      alert("Signup failed!");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-4">Signup</h1>
      <form onSubmit={handleSignup} className="w-80 space-y-4">
        <input
          className="w-full border p-2 rounded"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          className="w-full border p-2 rounded"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          className="w-full border p-2 rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button
          type="submit"
          className="w-full bg-green-600 text-white p-2 rounded"
        >
          Signup
        </button>
      </form>
      <p className="mt-4 text-sm">
        Already have an account?{" "}
        <Link to="/login" className="text-blue-600 underline">
          Log in
        </Link>
      </p>
    </div>
  );
}
