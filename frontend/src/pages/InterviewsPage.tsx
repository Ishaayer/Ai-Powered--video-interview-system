import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { interviewService } from "@/services/interview.service";

import Loading from "@/components/common/Loading";
import {
  Calendar,
  Clock,
  PlayCircle,
  Search,
  Filter,
  Briefcase,
  CheckCircle,
  Timer,
} from "lucide-react";

export default function InterviewsPage() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [interviews, setInterviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const totalInterviews = interviews.length;

  const completedInterviews = interviews.filter(
    (item) => item.status === "completed"
  ).length;

  const activeInterviews = interviews.filter(
    (item) => item.status !== "completed"
  ).length;

  const loadInterviews = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log("🔄 Loading interviews...");

      const data = await interviewService.getInterviews();
      console.log("✅ Interviews loaded:", data);

      setInterviews(data || []);
    } catch (error) {
      console.error("❌ Error loading interviews:", error);
      setError("Failed to load interviews. Please try again.");
      setInterviews([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInterviews();
  }, []);

  const filtered = interviews.filter((item) =>
    item.topic?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg font-medium mb-4">{error}</p>
          <button
            onClick={loadInterviews}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">
        <div>
          <h1 className="text-3xl font-bold">Interviews</h1>
          <p className="text-slate-500 mt-2">
            View and manage all your interview sessions.
          </p>
        </div>

        <button
          onClick={() => navigate("/start-interview")}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl shadow"
        >
          <PlayCircle size={20} />
          Start Interview
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow border p-6">
          <Calendar className="text-blue-600 mb-3" />
          <h2 className="text-3xl font-bold">{totalInterviews}</h2>
          <p className="text-slate-500">Total Interviews</p>
        </div>

        <div className="bg-white rounded-xl shadow border p-6">
          <Timer className="text-orange-500 mb-3" />
          <h2 className="text-3xl font-bold">{activeInterviews}</h2>
          <p className="text-slate-500">Scheduled</p>
        </div>

        <div className="bg-white rounded-xl shadow border p-6">
          <CheckCircle className="text-green-600 mb-3" />
          <h2 className="text-3xl font-bold">{completedInterviews}</h2>
          <p className="text-slate-500">Completed</p>
        </div>
      </div>

      <div className="bg-white rounded-xl border shadow p-5">
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search
              size={18}
              className="absolute left-3 top-3 text-gray-400"
            />
            <input
              type="text"
              placeholder="Search interviews..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full border rounded-lg py-2 pl-10 pr-3"
            />
          </div>

          <button className="flex items-center justify-center gap-2 border rounded-lg px-5 py-2 hover:bg-slate-100">
            <Filter size={18} />
            Filter
          </button>
        </div>

        <div className="space-y-5">
          {filtered.length === 0 ? (
            <p className="text-slate-500 text-center py-8">
              No interviews found
            </p>
          ) : (
            filtered.map((item) => (
              <div
                key={item.id}
                className="border rounded-xl p-5 hover:shadow-md transition"
              >
                <div className="flex flex-col md:flex-row md:justify-between gap-4">
                  <div>
                    <h2 className="text-xl font-semibold">{item.topic}</h2>
                    <div className="flex items-center gap-2 text-slate-500 mt-2">
                      <Briefcase size={16} />
                      {item.difficulty}
                    </div>

                    <div className="flex gap-6 mt-4 text-sm text-slate-500">
                      <div className="flex items-center gap-2">
                        <Calendar size={16} />
                        {new Date(item.created_at).toLocaleDateString()}
                      </div>

                      <div className="flex items-center gap-2">
                        <Clock size={16} />
                        Status: {item.status}
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col items-end justify-between">
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        item.status === "completed"
                          ? "bg-green-100 text-green-700"
                          : "bg-blue-100 text-blue-700"
                      }`}
                    >
                      {item.status}
                    </span>

                    <button
                      onClick={() => navigate(`/interviews/${item.id}`)}
                      className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
                    >
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}