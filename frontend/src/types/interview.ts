export interface Interview {
  id: number;
  candidate_id: number;
  topic: string;
  difficulty: string;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}