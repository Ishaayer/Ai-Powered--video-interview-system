export interface Report {
  id: number;
  interview_id: number;
  summary: string | null;
  strengths: string | null;
  weaknesses: string | null;
  recommendations: string | null;
  created_at: string;
}