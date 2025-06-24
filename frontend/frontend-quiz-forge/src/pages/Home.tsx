import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import type { Variants } from "framer-motion";

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 1) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.15,
      duration: 0.6,
      ease: [0.16, 1, 0.3, 1], // More springy animation
    },
  }),
};

export default function Home() {
  const { userId } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
      {/* Hero Section */}
      <section className="relative text-center py-24 px-4 overflow-hidden">
        {/* Animated background elements */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="absolute inset-0 overflow-hidden pointer-events-none"
        >
          {/* Floating gradient circles */}
          <motion.div
            animate={{
              x: [0, 20, 0],
              y: [0, -30, 0],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-gradient-to-r from-indigo-400/20 to-blue-400/20 blur-3xl"
          />
          <motion.div
            animate={{
              x: [0, -30, 0],
              y: [0, 40, 0],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 2
            }}
            className="absolute bottom-1/4 right-1/4 w-72 h-72 rounded-full bg-gradient-to-r from-purple-400/20 to-pink-400/20 blur-3xl"
          />
        </motion.div>

        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeUp}
          className="max-w-5xl mx-auto relative z-10"
        >
          <motion.h1
            className="text-6xl md:text-7xl lg:text-8xl font-bold mb-8"
            variants={fadeUp}
            custom={1}
            whileHover={{
              scale: 1.02,
              transition: { duration: 0.3 }
            }}
          >
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-blue-500">
              QuizForge
            </span>
          </motion.h1>

          <motion.p
            className="text-2xl md:text-3xl mb-10 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed"
            variants={fadeUp}
            custom={2}
          >
            Transform <span className="font-semibold text-indigo-600 dark:text-indigo-400">any content</span> into an interactive{" "}
            <span className="font-semibold text-blue-600 dark:text-blue-400">learning experience</span> in seconds
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row justify-center gap-4"
            variants={fadeUp}
            custom={3}
            whileInView={{
              scale: [0.95, 1],
              transition: { duration: 0.5 }
            }}
          >
            {userId ? (
              <>
                <Button
                  onClick={() => navigate("/upload")}
                  className="bg-indigo-600 hover:bg-indigo-700 px-8 py-4 text-lg shadow-lg transition-all hover:scale-105"
                >
                  Create a Quiz
                </Button>
                <Button
                  variant="outline"
                  onClick={() => navigate("/join")}
                  className="border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-50 dark:border-indigo-400 dark:text-indigo-400 dark:hover:bg-indigo-900/30 px-8 py-4 text-lg transition-all"
                >
                  Join Quiz
                </Button>
              </>
            ) : (
              <>
                <Button
                  onClick={() => navigate("/login")}
                  className="bg-indigo-600 hover:bg-indigo-700 px-8 py-4 text-lg shadow-lg transition-all hover:scale-105"
                >
                  Get Started
                </Button>
                <Button
                  variant="outline"
                  onClick={() => navigate("/signup")}
                  className="border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-50 dark:border-indigo-400 dark:text-indigo-400 dark:hover:bg-indigo-900/30 px-8 py-4 text-lg transition-all"
                >
                  Sign Up Free
                </Button>
              </>
            )}
          </motion.div>
        </motion.div>

        {/* Floating animated shapes */}
        <motion.div
          animate={{
            y: [0, -20, 0],
            rotate: [0, 5, 0]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute bottom-20 left-10 w-16 h-16 rounded-lg bg-indigo-400/10 backdrop-blur-sm border border-indigo-200/20 pointer-events-none"
        />
        <motion.div
          animate={{
            y: [0, 30, 0],
            rotate: [0, -8, 0]
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1
          }}
          className="absolute top-32 right-16 w-12 h-12 rounded-full bg-blue-400/10 backdrop-blur-sm border border-blue-200/20 pointer-events-none"
        />
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-6 bg-gradient-to-b from-white via-indigo-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-500">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            className="text-4xl font-bold text-center text-indigo-700 dark:text-indigo-400 relative mb-16"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeUp}
          >
            <span className="relative inline-block">
              <span className="absolute -bottom-2 left-0 right-0 h-2 bg-gradient-to-r from-indigo-400 to-blue-400 rounded-full"></span>
              <span className="relative bg-white dark:bg-gray-900 px-6">How It Works</span>
            </span>
          </motion.h2>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: "📄",
                title: "Upload Content",
                description: "Upload PDFs, text, or URLs. Set your preferences for question types and difficulty.",
                bg: "from-indigo-50 to-white dark:from-indigo-900/20 dark:to-gray-800",
                delay: 0.1
              },
              {
                icon: "🤖",
                title: "AI Generates Quiz",
                description: "Our AI analyzes your content and creates tailored questions with explanations.",
                bg: "from-blue-50 to-white dark:from-blue-900/20 dark:to-gray-800",
                delay: 0.2
              },
              {
                icon: "🎯",
                title: "Learn & Compete",
                description: "Take the quiz solo or with friends, track progress, and earn achievements.",
                bg: "from-purple-50 to-white dark:from-purple-900/20 dark:to-gray-800",
                delay: 0.3
              },
            ].map((step, index) => (
              <motion.div
                key={index}
                className={`bg-gradient-to-b ${step.bg} rounded-2xl p-8 shadow-xl border border-gray-200/70 dark:border-gray-700/50 hover:shadow-2xl transition-all duration-300 group`}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                custom={index + 1}
                whileHover={{ y: -10 }}
              >
                <div className="text-4xl w-14 h-14 flex items-center justify-center rounded-full bg-gradient-to-br from-indigo-600 to-blue-500 text-white mb-4 shadow-lg group-hover:scale-110 transition-transform">
                  {step.icon}
                </div>
                <h3 className="text-2xl font-semibold text-indigo-700 dark:text-indigo-300 mb-2">{step.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-6 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            className="text-4xl font-bold text-center mb-16 text-indigo-700 dark:text-indigo-400"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeUp}
          >
            <span className="relative inline-block">
              <span className="absolute -bottom-2 left-0 right-0 h-2 bg-gradient-to-r from-indigo-400 to-blue-400 rounded-full"></span>
              <span className="relative px-4 bg-gray-50 dark:bg-gray-900">Why QuizForge?</span>
            </span>
          </motion.h2>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { 
                icon: "🎯", 
                title: "Personalized Learning", 
                description: "Quizzes tailored to your content and preferences",
                color: "from-indigo-100 to-indigo-50 dark:from-indigo-900/30 dark:to-gray-800" 
              },
              { 
                icon: "🔐", 
                title: "Secure & Private", 
                description: "Your data stays yours with enterprise-grade security",
                color: "from-blue-100 to-blue-50 dark:from-blue-900/30 dark:to-gray-800" 
              },
              { 
                icon: "🏆", 
                title: "Gamified Learning", 
                description: "Leaderboards, badges, and achievements to motivate",
                color: "from-purple-100 to-purple-50 dark:from-purple-900/30 dark:to-gray-800" 
              },
              { 
                icon: "💡", 
                title: "Instant Feedback", 
                description: "Detailed explanations for every answer",
                color: "from-teal-100 to-teal-50 dark:from-teal-900/30 dark:to-gray-800" 
              },
            ].map((benefit, index) => (
              <motion.div
                key={index}
                className={`bg-gradient-to-b ${benefit.color} rounded-xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-200/50 dark:border-gray-700/30 group`}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                custom={index + 1}
                whileHover={{ y: -5 }}
              >
                <div className="text-4xl mb-4 transition-transform group-hover:scale-110">{benefit.icon}</div>
                <h3 className="text-xl font-semibold text-indigo-700 dark:text-indigo-300 mb-2">{benefit.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{benefit.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>


      {/* CTA Section */}
      <section className="relative py-24 px-6 bg-gradient-to-br from-indigo-600 to-blue-600 text-white overflow-hidden">
        <div className="absolute inset-0 bg-noise opacity-10 pointer-events-none"></div>
        <div className="max-w-4xl mx-auto relative z-10 text-center">
          <motion.h2
            className="text-3xl md:text-4xl font-bold mb-6"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
          >
            Ready to Transform Your Learning?
          </motion.h2>
          <motion.p
            className="text-xl mb-10 opacity-90 max-w-2xl mx-auto"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            custom={1}
          >
            Join thousands of users who are learning smarter with QuizForge
          </motion.p>
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            custom={2}
            className="flex justify-center"
          >
            <Button
              onClick={() => navigate(userId ? "/upload" : "/signup")}
              className="bg-white text-indigo-600 hover:bg-indigo-50 px-8 py-4 text-lg font-semibold rounded-xl shadow-xl transition-all hover:scale-105"
            >
              {userId ? "Create a Quiz Now" : "Get Started Free"}
            </Button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center py-8 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
        <div className="max-w-6xl mx-auto px-6">
          <motion.p
            className="text-sm text-gray-500 dark:text-gray-400"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
          >
            Built with ❤️ by Rishitha · Powered by DeepSeek via OpenRouter
          </motion.p>
        </div>
      </footer>
    </div>
  );
}