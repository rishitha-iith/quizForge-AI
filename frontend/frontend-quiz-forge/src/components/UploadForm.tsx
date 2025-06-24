import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { generateQuiz } from "@/services/api/quiz";
import { Switch } from "@/components/ui/switch";
import { toast } from "sonner";
import { useAuth } from "@/context/AuthContext";
import { motion } from "framer-motion";
import {
  FiUpload,
  FiClock,
  FiUsers,
  FiFileText,
  FiAward,
} from "react-icons/fi";

export default function UploadForm() {
  const { token } = useAuth();
  const navigate = useNavigate();

  const [quizName, setQuizName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [numQuestions, setNumQuestions] = useState(5);
  const [numUsers, setNumUsers] = useState(1);
  const [difficulty, setDifficulty] = useState("medium");
  const [duration, setDuration] = useState("");
  const [aiSuggestTime, setAiSuggestTime] = useState(true);
  const [loading, setLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const handleGenerateQuiz = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!token || !quizName || !file) {
      toast.error("Please fill all required fields");
      return;
    }

    if (!aiSuggestTime && !duration) {
      toast.error("Please enter duration or let AI suggest it");
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("token", token);
      formData.append("quiz_name", quizName);
      formData.append("num_questions", String(numQuestions));
      formData.append("num_users", String(numUsers));
      formData.append("difficulty", difficulty);
      formData.append("duration_minutes", aiSuggestTime ? "0" : duration);
      formData.append("file", file);

      const response = await generateQuiz(formData);

      toast.success("Quiz generated successfully!");

      navigate(`/start-quiz/${response.quiz_id}`, {
        state: {
          quiz_id: response.quiz_id,
          quiz_name: response.quiz_name,
          difficulty: response.difficulty,
          duration_minutes: response.duration_minutes,
          message: response.message,
        },
      });
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || "Failed to generate quiz.");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === "application/pdf") {
      setFile(droppedFile);
    } else {
      toast.error("Please upload a PDF file");
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <motion.div
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-10">
          <h2 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 mb-4">
            Craft Your Perfect Quiz
          </h2>
          <p className="text-lg text-blue-600/80">
            Transform your content into an engaging learning experience
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden border border-blue-100 dark:border-gray-700">
          <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-5 text-white">
            <h3 className="text-xl font-semibold flex items-center gap-2">
              <FiFileText />
              Quiz Configuration
            </h3>
          </div>

          <form onSubmit={handleGenerateQuiz} className="p-6 space-y-6">
            <div>
              <Label htmlFor="quizName" className="flex gap-2 items-center text-blue-700">
                <FiAward />
                Quiz Name
              </Label>
              <Input
                id="quizName"
                value={quizName}
                onChange={(e) => setQuizName(e.target.value)}
                required
              />
            </div>

            <div
              className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all ${
                isDragging
                  ? "border-blue-500 bg-blue-50"
                  : "border-blue-200"
              }`}
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => document.getElementById("file")?.click()}
            >
              {file ? (
                <>
                  <p className="font-medium text-blue-700">{file.name}</p>
                  <p className="text-sm text-blue-500/70">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </>
              ) : (
                <>
                  <FiUpload className="mx-auto h-10 w-10 text-blue-400 mb-2" />
                  <p className="text-blue-600">Drag & drop PDF here or click to upload</p>
                  <p className="text-xs text-blue-400 mt-1">Only .pdf files (max 10MB)</p>
                </>
              )}
              <Input
                id="file"
                type="file"
                accept="application/pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="numQuestions">Number of Questions</Label>
                <Input
                  id="numQuestions"
                  type="number"
                  min={1}
                  max={20}
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(Number(e.target.value))}
                  required
                />
              </div>

              <div>
                <Label htmlFor="numUsers">Number of Users</Label>
                <Input
                  id="numUsers"
                  type="number"
                  min={1}
                  max={50}
                  value={numUsers}
                  onChange={(e) => setNumUsers(Number(e.target.value))}
                  required
                />
              </div>
            </div>

            <div>
              <Label>Difficulty</Label>
              <Select value={difficulty} onValueChange={setDifficulty}>
                <SelectTrigger>
                  <SelectValue placeholder="Select difficulty" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="easy">Easy</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="hard">Hard</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center justify-between">
              <Label htmlFor="aiTime" className="flex items-center gap-2">
                <FiClock />
                Let AI Suggest Time
              </Label>
              <Switch
                id="aiTime"
                checked={aiSuggestTime}
                onCheckedChange={setAiSuggestTime}
              />
            </div>

            {!aiSuggestTime && (
              <div>
                <Label htmlFor="duration">Duration (in minutes)</Label>
                <Input
                  id="duration"
                  type="number"
                  min={1}
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  required
                />
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all"
              disabled={loading}
            >
              {loading ? "Generating Quiz..." : "Generate Quiz Now"}
            </Button>
          </form>
        </div>
      </motion.div>
    </div>
  );
}
