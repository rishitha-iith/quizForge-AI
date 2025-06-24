import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser } from "@/services/api/auth";
import { useAuth } from "../context/AuthContext";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FcGoogle } from "react-icons/fc";
import { Eye, EyeOff } from "lucide-react";
import { toast } from "sonner";
import { Loader2, CheckCircle2, AlertCircle, Rocket } from "lucide-react";

export default function LoginPage() {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const { setUserId } = useAuth();
  const navigate = useNavigate();

   const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  const toastId = toast.loading(
    <div className="flex flex-col">
      <span className="font-semibold">Authenticating</span>
      <span className="text-sm text-gray-500">Please wait while we verify your credentials</span>
    </div>,
    {
      style: {
        background: 'rgba(236, 253, 245, 0.9)',
        border: '1px solid #a7f3d0',
        color: '#065f46',
        backdropFilter: 'blur(4px)',
      },
    }
  );

  try {
    const response = await loginUser(identifier, password);
    setUserId(response.user_id);
    localStorage.setItem("user_id", response.user_id);
    localStorage.setItem("token", response.token);

    toast.dismiss(toastId);
    toast.success(
      <div className="flex flex-col">
        <span className="font-semibold">Welcome back!</span>
        <span className="text-sm text-gray-600">You've been successfully logged in</span>
      </div>,
      {
        style: {
          background: 'rgba(236, 253, 245, 0.9)',
          border: '1px solid #6ee7b7',
          color: '#065f46',
          backdropFilter: 'blur(4px)',
        },
        // icon: '🎉',
        duration: 3000,
      }
    );
    navigate("/home");
  } catch (error) {
    toast.dismiss(toastId);
    toast.error(
      <div className="flex flex-col">
        <span className="font-semibold">Login failed</span>
        <span className="text-sm text-gray-600">Please check your credentials and try again</span>
      </div>,
      {
        style: {
          background: 'rgba(254, 226, 226, 0.9)',
          border: '1px solid #fca5a5',
          color: '#b91c1c',
          backdropFilter: 'blur(4px)',
        },
        // icon: '❌',
        duration: 4000,
      }
    );
  }
};


  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4 relative overflow-hidden">
      {/* Decorative blobs */}
      <div className="absolute top-0 left-0 w-64 h-64 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
      <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
      <div className="absolute bottom-0 left-1/2 w-64 h-64 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>

      <div className="relative w-full max-w-sm">
        <div className="absolute top-3 left-3 w-full h-full bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl transform rotate-3 scale-105 z-0 shadow-2xl transition duration-500" />
        <div className="relative z-10 bg-white/90 backdrop-blur-sm p-8 rounded-xl shadow-lg transform transition duration-300 hover:scale-[1.02] hover:shadow-2xl border border-white/20">
          <h2 className="text-3xl font-bold text-gray-800 text-center mb-6">Welcome Back</h2>
          <p className="text-center text-gray-500 mb-6">Sign in to your account</p>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="identifier" className="block text-sm font-medium text-gray-700 mb-1">
                Email or Username
              </label>
              <Input
                id="identifier"
                type="text"
                placeholder="you@example.com"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                required
                className="text-sm"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="pr-10 text-sm"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-2 flex items-center text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div className="flex justify-end text-sm">
              <Link to="/forgot-password" className="text-blue-600 hover:underline">
                Forgot password?
              </Link>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-medium shadow-md hover:shadow-lg transition-all duration-300"
            >
              Sign In
            </Button>
          </form>

          <div className="text-center text-sm text-gray-500 mt-4">
            Don't have an account?{" "}
            <Link to="/signup" className="text-blue-600 hover:underline font-medium">
              Sign up
            </Link>
          </div>

          <div className="flex items-center gap-2 my-4">
            <hr className="flex-grow border-gray-300" />
            <span className="text-gray-400 text-xs">OR</span>
            <hr className="flex-grow border-gray-300" />
          </div>

          <Button
            variant="outline"
            type="button"
            className="w-full flex items-center justify-center gap-2 text-sm"
          >
            <FcGoogle className="text-xl" />
            Continue with Google
          </Button>
        </div>
      </div>
    </div>
  );
}
