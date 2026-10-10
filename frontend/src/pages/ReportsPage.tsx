import { useState } from "react";
import { reportService } from "@/services/report.service";
import { scoreService } from "@/services/score.service";

import type { Report } from "@/types/report";
import type { Score } from "@/types/score";
import {
  FileText,
  Search,
  Download,
  Brain,
  MessageSquare,
  Award,
} from "lucide-react";

export default function ReportsPage() {

  const [interviewId, setInterviewId] = useState("");

  const [report, setReport] = useState<Report | null>(null);

  const [score, setScore] = useState<Score | null>(null);

  const [loading, setLoading] = useState(false);


  const loadReport = async () => {

    if (!interviewId) return;

    try {

      setLoading(true);

      const reportData =
        await reportService.getReport(interviewId);

      const scoreData =
        await scoreService.getScore(interviewId);


      setReport(reportData);

      setScore(scoreData);

    } catch (error) {

      console.error(error);

      alert("Report not found.");

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="space-y-8">


      <div>

        <h1 className="text-3xl font-bold">
          Interview Reports
        </h1>

        <p className="text-slate-500 mt-2">
          View AI-generated interview reports.
        </p>

      </div>



      <div className="bg-white border rounded-2xl shadow p-6">

        <div className="flex gap-3">


          <div className="relative flex-1">

            <Search
              size={18}
              className="absolute left-3 top-3 text-gray-400"
            />


            <input
              type="number"
              placeholder="Enter Interview ID..."
              value={interviewId}
              onChange={(e) =>
                setInterviewId(e.target.value)
              }
              className="w-full border rounded-lg py-2 pl-10 pr-3"
            />

          </div>


          <button
            onClick={loadReport}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 rounded-lg"
          >
            Load Report
          </button>


        </div>

      </div>




      {
        loading && (

          <div className="text-center">
            Loading...
          </div>

        )
      }





      {
        report && (

          <>


            <div className="grid md:grid-cols-4 gap-6">

              <div className="bg-white border rounded-xl p-6">

                <Award
                  className="text-green-600 mb-3"
                />

                <h2 className="text-3xl font-bold">
                  {score?.overall_score ?? "N/A"}
                </h2>

                <p className="text-slate-500">
                  Overall Score
                </p>

              </div>


              <div className="bg-white border rounded-xl p-6">

                <Brain
                  className="text-blue-600 mb-3"
                />

                <h2 className="font-semibold">
                  Strengths
                </h2>


                <p className="mt-3 text-slate-600">
                  {report.strengths}
                </p>


              </div>




              <div className="bg-white border rounded-xl p-6">

                <Brain
                  className="text-red-600 mb-3"
                />

                <h2 className="font-semibold">
                  Weaknesses
                </h2>


                <p className="mt-3 text-slate-600">
                  {report.weaknesses}
                </p>


              </div>





              <div className="bg-white border rounded-xl p-6">

                <MessageSquare
                  className="text-purple-600 mb-3"
                />

                <h2 className="font-semibold">
                  Recommendations
                </h2>


                <p className="mt-3 text-slate-600">
                  {report.recommendations}
                </p>


              </div>



            </div>






            <div className="bg-white border rounded-2xl p-6">


              <div className="flex justify-between items-center">


                <div>

                  <h2 className="text-2xl font-bold">
                    Report Summary
                  </h2>


                  <p className="text-slate-500 mt-1">
                    AI generated interview assessment
                  </p>


                </div>




                <button
                  className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
                >

                  <Download size={18} />

                  Download

                </button>


              </div>





              <div className="mt-6 flex items-start gap-3">


                <FileText className="text-blue-600"/>


                <p className="text-slate-700 leading-7">

                  {report.summary}

                </p>


              </div>



            </div>



          </>

        )
      }



    </div>

  );

}