export interface Score {
  id: number;
  interview_id: number;
  technical_score: number | null;
  communication_score: number | null;
  confidence_score: number | null;
  overall_score: number | null;
  created_at: string;
}