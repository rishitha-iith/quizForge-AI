import { CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import React from "react";

type Props = {
  index: number;
  question: string;
  options: string[];
  correct_answer: string;
  user_answer: string;
  explanation: string;
  isFlipped: boolean;
  onFlip: () => void;
  onExpand: () => void;
};

export const ExplanationCard: React.FC<Props> = ({
  index,
  question,
  options,
  correct_answer,
  user_answer,
  explanation,
  isFlipped,
  onFlip,
  onExpand,
}) => {
  const isCorrect = user_answer === correct_answer;
  const bgColor = isCorrect ? "bg-green-50 border-green-400" : "bg-red-50 border-red-400";
  const cardHeight = "min-h-[300px]";

  return (
    <motion.div
      className={`rounded-xl overflow-hidden shadow-md border ${bgColor} ${cardHeight} relative`}
      style={{ perspective: 1000 }}
    >
      <motion.div
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6 }}
        className="relative w-full h-full"
        style={{ transformStyle: "preserve-3d" }}
      >
        {/* Front Side */}
        <div className="absolute w-full h-full p-6 backface-hidden">
          <CardContent>
            <h2 className="text-md font-semibold mb-4">Q{index + 1}. {question}</h2>
            <ul className="list-disc list-inside space-y-1 text-sm">
              {options.map((opt, i) => (
                <li
                  key={i}
                  className={
                    opt === correct_answer
                      ? "text-green-600 font-semibold"
                      : opt === user_answer
                      ? "text-red-600"
                      : ""
                  }
                >
                  {opt}
                </li>
              ))}
            </ul>
            <p className="mt-4 text-sm">
              <strong>Your Answer:</strong>{" "}
              <span className={isCorrect ? "text-green-700" : "text-red-700"}>
                {user_answer || "Not answered"}
              </span>
            </p>
            <Button variant="outline" className="mt-4" onClick={onFlip}>
              Get Explanation
            </Button>
          </CardContent>
        </div>

        {/* Back Side */}
        <div
          className="absolute w-full h-full p-6 backface-hidden transform rotateY-180"
          style={{
            background: "#fff",
            borderRadius: "inherit",
            overflowY: "auto",
          }}
        >
          <CardContent className="flex flex-col justify-between h-full">
            <div className="mb-4">
              <h3 className="text-md font-semibold mb-2">Explanation:</h3>
              <p className="text-sm line-clamp-4">
                {explanation}
              </p>
              {explanation.length > 300 && (
                <Button
                  variant="link"
                  className="mt-2 p-0 text-blue-600 text-sm"
                  onClick={onExpand}
                >
                  Learn more
                </Button>
              )}
            </div>
            <Button variant="outline" onClick={onFlip} className="self-end">
              Back to Question
            </Button>
          </CardContent>
        </div>
      </motion.div>
    </motion.div>
  );
};
