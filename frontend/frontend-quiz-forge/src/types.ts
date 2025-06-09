export interface Question {
  question: string;
  options: string[];
  correct_index: number;
}

export interface Quiz {
  title: string;
  questions: Question[];
}

export interface UserResponse {
  user_id: string;
  quiz_id: number;
  answers: Record<number, string>;
  time_taken: number;
}
