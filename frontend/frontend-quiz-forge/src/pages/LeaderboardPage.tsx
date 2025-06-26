import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getOverallLeaderboard, getQuizLeaderboard } from "@/services/api/leaderboard";
import { getUserBadges } from "@/services/api/badges";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

interface QuizLeaderboardEntry {
  username?: string;
  score: number;
  accuracy: number;
}

interface OverallLeaderboardEntry {
  username: string;
  average_score: number;
}

export default function LeaderboardPage() {
  const { quizCode } = useParams<{ quizCode: string }>();

  const userId = localStorage.getItem("user_id") || "";
  const [quizLeaderboard, setQuizLeaderboard] = useState<QuizLeaderboardEntry[]>([]);
  const [overallLeaderboard, setOverallLeaderboard] = useState<OverallLeaderboardEntry[]>([]);
  const [badges, setBadges] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [quizLb, overallLb, badgeRes] = await Promise.all([
          getQuizLeaderboard(quizCode!), // 🛠️ Use quiz_name from route
          getOverallLeaderboard(),
          getUserBadges(userId),
        ]);

        setQuizLeaderboard(quizLb.leaderboard || []);
        setOverallLeaderboard(overallLb || []);
        setBadges(badgeRes.badges || []);
      } catch (error) {
        toast.error("Failed to load leaderboard or badges.");
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [quizCode, userId]);

  const renderQuizLeaderboard = () => (
    <div className="grid gap-4">
      {quizLeaderboard.map((entry, index) => (
        <Card key={index} className="border p-4">
          <CardContent>
            <p className="font-semibold">
              {index + 1}. {entry.username ?? "Anonymous"}
            </p>
            <p className="text-sm">
              Score: {entry.score} | Accuracy: {entry.accuracy}%
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );

  const renderOverallLeaderboard = () => (
    <div className="grid gap-4">
      {overallLeaderboard.map((entry, index) => (
        <Card key={index} className="border p-4">
          <CardContent>
            <p className="font-semibold">
              {index + 1}. {entry.username}
            </p>
            <p className="text-sm">
              Average Score: {entry.average_score}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );

  const renderBadges = () => (
    <div className="flex flex-wrap gap-3 mt-6">
      {badges.length > 0 ? (
        badges.map((badge, i) => (
          <Badge key={i} variant="secondary" className="text-sm px-3 py-1">
            🏅 {badge}
          </Badge>
        ))
      ) : (
        <p className="text-sm text-muted-foreground">No badges yet.</p>
      )}
    </div>
  );

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center text-indigo-700 dark:text-white">
        Leaderboard & Badges
      </h1>

      {loading ? (
        <p className="text-center">Loading leaderboard...</p>
      ) : (
        <Tabs defaultValue="quiz" className="w-full">
          <TabsList className="flex justify-center gap-4 mb-6">
            <TabsTrigger value="quiz">This Quiz</TabsTrigger>
            <TabsTrigger value="overall">Overall</TabsTrigger>
            <TabsTrigger value="badges">Your Badges</TabsTrigger>
          </TabsList>

          <TabsContent value="quiz">{renderQuizLeaderboard()}</TabsContent>
          <TabsContent value="overall">{renderOverallLeaderboard()}</TabsContent>
          <TabsContent value="badges">{renderBadges()}</TabsContent>
        </Tabs>
      )}
    </div>
  );
}
