export interface Question {
  id: number;
  interview_id: number;
  question_text: string;
  topic: string;
  difficulty: string;
  category: string | null;
}