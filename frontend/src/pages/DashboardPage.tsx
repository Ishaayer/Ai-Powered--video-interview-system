import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  ClipboardList,
  FileText,
  BarChart3,
  CheckCircle2,
  PlayCircle,
  User,
  CheckCircle,
} from "lucide-react";

import resumeService from "@/services/resume.service";
import { interviewService } from "@/services/interview.service";

import PageHeader from "@/components/common/PageHeader";
import StatCard from "@/components/common/StatCard";
import SectionCard from "@/components/common/SectionCard";
import PrimaryButton from "@/components/common/PrimaryButton";

interface Interview {
  id: number;
  candidate_id: number;
  topic: string;
  difficulty: string;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

interface Resume {
  id: number;
  candidate_id: number;
  file_name: string;
  file_url: string;
  file_type: string;
  file_size: number;
  uploaded_at: string;
}

export default function DashboardPage() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);

  const [interviews, setInterviews] = useState<Interview[]>([]);

  const [resumeUploaded, setResumeUploaded] =
    useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      setLoading(true);

      const interviewData =
        await interviewService.getInterviews();

      setInterviews(interviewData);

      try {
        await resumeService.getResume();
        setResumeUploaded(true);
      } catch {
        setResumeUploaded(false);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to load dashboard.");
    } finally {
      setLoading(false);
    }
  }

  const totalInterviews = interviews.length;

  const completedInterviews = interviews.filter(
    (i) => i.status.toLowerCase() === "completed"
  ).length;

  const reportsCount = completedInterviews;

  const recentInterviews = [...interviews]
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() -
        new Date(a.created_at).getTime()
    )
    .slice(0, 5);

  const lastInterview =
    recentInterviews.length > 0
      ? recentInterviews[0]
      : null;

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        Loading Dashboard...
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-600">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-8">

      <PageHeader
        title="Dashboard"
        subtitle="Welcome back. Here's an overview of your interview progress."
      />

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

        <StatCard
          title="Total Interviews"
          value={totalInterviews}
          icon={ClipboardList}
        />

        <StatCard
          title="Completed"
          value={completedInterviews}
          icon={CheckCircle2}
        />

        <StatCard
          title="Reports"
          value={reportsCount}
          icon={BarChart3}
        />

        <StatCard
          title="Resume Uploaded"
          value={resumeUploaded ? "Yes" : "No"}
          icon={FileText}
        />

      </div>

      <div className="grid gap-6 xl:grid-cols-3">

        <div className="xl:col-span-2">

          <SectionCard title="Recent Interviews">

            <div className="overflow-x-auto">

              <table className="w-full">

                <thead>

                  <tr className="border-b">

                    <th className="py-3 text-left">
                      Topic
                    </th>

                    <th className="py-3 text-left">
                      Date
                    </th>

                    <th className="py-3 text-left">
                      Status
                    </th>

                    <th className="py-3 text-left">
                      Score
                    </th>

                  </tr>

                </thead>

                <tbody>


                                    {recentInterviews.length === 0 ? (

                    <tr>

                      <td
                        colSpan={4}
                        className="py-8 text-center text-slate-500"
                      >
                        No interviews found.
                      </td>

                    </tr>

                  ) : (

                    recentInterviews.map((item) => (

                      <tr
                        key={item.id}
                        className="border-b last:border-0"
                      >

                        <td className="py-4 font-medium">
                          {item.topic}
                        </td>

                        <td>
                          {new Date(
                            item.created_at
                          ).toLocaleDateString()}
                        </td>

                        <td>

                          <span
                            className={`rounded-full px-3 py-1 text-sm ${
                              item.status.toLowerCase() === "completed"
                                ? "bg-green-100 text-green-700"
                                : item.status.toLowerCase() === "started"
                                ? "bg-blue-100 text-blue-700"
                                : "bg-yellow-100 text-yellow-700"
                            }`}
                          >
                            {item.status}
                          </span>

                        </td>

                        <td className="font-semibold">

                          {item.status.toLowerCase() === "completed"
                            ? "--"
                            : "--"}

                        </td>

                      </tr>

                    ))

                  )}

                </tbody>

              </table>

            </div>

          </SectionCard>

        </div>

        <SectionCard title="Quick Actions">

          <div className="space-y-4">

            <PrimaryButton
              className="flex w-full items-center justify-center gap-2"
              onClick={() => navigate("/start-interview")}
            >

              <PlayCircle size={20} />

              Start New Interview

            </PrimaryButton>

            <button
              onClick={() => navigate("/reports")}
              className="w-full rounded-xl border border-slate-300 bg-white px-6 py-3 font-medium transition hover:bg-slate-100"
            >

              View Reports

            </button>

            <button
              onClick={() => navigate("/profile")}
              className="w-full rounded-xl border border-slate-300 bg-white px-6 py-3 font-medium transition hover:bg-slate-100"
            >

              Update Profile

            </button>

          </div>

          <div className="mt-8 rounded-xl bg-blue-50 p-5">

            <div className="space-y-4">

              <div className="flex items-center gap-3">

                <User
                  size={20}
                  className="text-blue-600"
                />

                <div>

                  <p className="font-semibold">

                    Current Status

                  </p>

                  <p className="text-sm text-slate-500">

                    Your interview progress

                  </p>

                </div>

              </div>

              <div className="space-y-2 text-sm">

                <div className="flex items-center gap-2">

                  <CheckCircle
                    size={18}
                    className="text-green-600"
                  />

                  <span>
                    Resume{" "}
                    {resumeUploaded
                      ? "Uploaded"
                      : "Not Uploaded"}
                  </span>

                </div>

                <div className="flex items-center gap-2">

                  <CheckCircle
                    size={18}
                    className="text-green-600"
                  />

                  <span>
                    Interviews Completed:{" "}
                    {completedInterviews}
                  </span>

                </div>

                {lastInterview && (

                  <>
                    <hr />

                    <div>

                      <p className="font-medium">
                        Last Interview
                      </p>

                      <p>
                        {lastInterview.topic}
                      </p>

                    </div>

                    <div>

                      <p className="font-medium">
                        Status
                      </p>

                      <p>
                        {lastInterview.status}
                      </p>

                    </div>

                  </>

                )}

              </div>

            </div>

          </div>

        </SectionCard>

      </div>

    </div>

  );

}