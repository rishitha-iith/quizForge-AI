import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getExplanations } from "@/services/api/explanations";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import { ExplanationCard } from "@/components/ExplanationCard";

type Explanation = {
  question: string;
  options: string[];
  correct_index: number;
  user_index: number | null;
  is_correct: boolean;
  explanation: string;
};

export default function ExplanationPage() {
  const { quizName, userId } = useParams<{ quizName: string; userId: string }>();
  const navigate = useNavigate();

  const [data, setData] = useState<Explanation[]>([]);
  const [flipped, setFlipped] = useState<Record<number, boolean>>({});
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    const fetchExplanations = async () => {
      try {
        const res = await getExplanations(quizName!, userId!);
        setData(res.explanations || []);
      } catch {
        toast.error("Failed to load explanations.");
      }
    };
    fetchExplanations();
  }, [quizName, userId]);

  const toggleFlip = (id: number) => {
    setFlipped((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleExpand = (id: number) => setExpanded(id);
  const handleCloseExpand = () => setExpanded(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-zinc-900 dark:to-zinc-800 p-6">
      <div className="flex justify-between items-center mb-6 max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-700 dark:text-white">Explanations</h1>
        <Button
          className="bg-indigo-600 hover:bg-indigo-700 text-white"
          onClick={() => navigate(`/leaderboard/${quizName}`)}
        >
          View Leaderboard
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
        {data.map((item, index) => (
          <ExplanationCard
            key={index}
            index={index}
            question={item.question}
            options={item.options}
            correct_answer={["A", "B", "C", "D"][item.correct_index]}
            user_answer={
              item.user_index !== null ? ["A", "B", "C", "D"][item.user_index] : "Not answered"
            }
            explanation={item.explanation}
            isFlipped={!!flipped[index]}
            onFlip={() => toggleFlip(index)}
            onExpand={() => handleExpand(index)}
          />
        ))}
      </div>

      {/* Fullscreen Explanation Modal */}
      <AnimatePresence>
        {expanded !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
          >
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.8 }}
              className="bg-white dark:bg-zinc-900 rounded-xl p-6 max-w-3xl w-full max-h-[90vh] overflow-y-auto relative"
            >
              <Button
                variant="ghost"
                className="absolute top-4 right-4 text-gray-500 hover:text-red-600"
                onClick={handleCloseExpand}
              >
                <X className="w-5 h-5" />
              </Button>
              <h2 className="text-lg font-bold mb-4 text-indigo-700">Full Explanation</h2>
              <p className="text-sm whitespace-pre-line">{data[expanded].explanation}</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
