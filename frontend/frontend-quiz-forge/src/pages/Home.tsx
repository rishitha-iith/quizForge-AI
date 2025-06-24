import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const { userId } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-indigo-50 dark:bg-gray-900 text-gray-900 dark:text-white transition-colors">
      {/* Hero Section */}
      <section className="text-center py-20 px-4 bg-white dark:bg-gray-800 shadow-sm">
        <h1 className="text-5xl md:text-6xl font-extrabold text-indigo-700 dark:text-indigo-400 mb-4 transition-all">
          QuizForge AI
        </h1>
        <p className="text-xl md:text-2xl mb-6 text-gray-700 dark:text-gray-300">
          Turn PDFs into AI-powered quizzes instantly!
        </p>
        <div className="space-x-4">
          {userId ? (
            <>
              <Button
                className="bg-indigo-600 hover:bg-indigo-700 text-white transition"
                onClick={() => navigate("/upload")}
              >
                Create a Quiz
              </Button>
              <Button
                variant="outline"
                className="border-indigo-600 text-indigo-600 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition"
                onClick={() => navigate("/join")}
              >
                Join Quiz
              </Button>
            </>
          ) : (
            <>
              <Button
                className="bg-indigo-600 hover:bg-indigo-700 text-white transition"
                onClick={() => navigate("/login")}
              >
                Login
              </Button>
              <Button
                variant="outline"
                className="border-indigo-600 text-indigo-600 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition"
                onClick={() => navigate("/signup")}
              >
                Sign Up
              </Button>
            </>
          )}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-indigo-100 dark:bg-gray-800 py-16 px-6 transition-colors">
        <h2 className="text-3xl font-bold text-center text-indigo-700 dark:text-indigo-400 mb-12">
          How It Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            {
              title: "📄 Upload a PDF",
              desc: "Choose number of questions, users, difficulty & time. Our AI reads the content.",
            },
            {
              title: "🤖 AI Generates Quiz",
              desc: "Smartly crafted questions tailored to your document and preferences.",
            },
            {
              title: "🧠 Start & Compete",
              desc: "Play solo or with friends, review answers, see leaderboard & earn badges!",
            },
          ].map(({ title, desc }) => (
            <div
              key={title}
              className="bg-white dark:bg-gray-700 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow"
            >
              <h3 className="text-xl font-semibold text-indigo-700 dark:text-indigo-300 mb-2">
                {title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Benefits */}
      <section className="py-16 px-6 bg-white dark:bg-gray-950 transition-colors">
        <h2 className="text-3xl font-bold text-center text-indigo-700 dark:text-indigo-400 mb-12">
          Why Use QuizForge?
        </h2>
        <ul className="grid sm:grid-cols-2 md:grid-cols-4 gap-6 max-w-6xl mx-auto text-center text-lg text-gray-700 dark:text-gray-300">
          <li>🎯 Personalized Quizzes</li>
          <li>🔐 Secure & Shareable</li>
          <li>🏆 Leaderboards & Gamification</li>
          <li>📊 Instant Explanations</li>
        </ul>
      </section>

      {/* Footer */}
      <footer className="text-center py-6 text-sm text-gray-500 dark:text-gray-400">
        Built by Rishitha 🚀 · Powered by DeepSeek via OpenRouter · v1.0
      </footer>
    </div>
  );
}
