import { useNavigate } from "react-router-dom";
import { interviewService } from "@/services/interview.service";


import {
  Video,
  Mic,
  Brain,
  Clock,
  Play,
  ShieldCheck,
} from "lucide-react";

export default function StartInterviewPage() {
  const navigate = useNavigate();

const startInterview = async () => {
  try {
    const interview = await interviewService.startInterview(
      "Python Fundamentals",
      "Beginner"
    );

    navigate(`/interviews/${interview.id}/session`);
  } catch (error) {
    console.error(error);

    alert("Unable to start interview.");
  }
};

  return (
    <div className="space-y-8">

      <div>
        <h1 className="text-3xl font-bold">
          Start Interview
        </h1>

        <p className="text-slate-500 mt-2">
          Complete your AI-powered interview assessment.
        </p>
      </div>


      <div className="bg-white border rounded-2xl shadow p-8 max-w-3xl">

        <div className="flex items-center gap-4 mb-8">

          <div className="bg-blue-100 p-4 rounded-xl">
            <Brain
              size={32}
              className="text-blue-600"
            />
          </div>

          <div>
            <h2 className="text-2xl font-semibold">
              AI Technical Interview
            </h2>

            <p className="text-slate-500">
              Python Fundamentals Assessment
            </p>
          </div>

        </div>



        <div className="grid md:grid-cols-2 gap-5">


          <div className="border rounded-xl p-5">

            <Video className="text-blue-600 mb-3"/>

            <h3 className="font-semibold">
              Video Recording
            </h3>

            <p className="text-sm text-slate-500 mt-2">
              Your video responses will be recorded and analysed by AI.
            </p>

          </div>



          <div className="border rounded-xl p-5">

            <Mic className="text-green-600 mb-3"/>

            <h3 className="font-semibold">
              Voice Analysis
            </h3>

            <p className="text-sm text-slate-500 mt-2">
              Speech and communication patterns will be evaluated.
            </p>

          </div>



          <div className="border rounded-xl p-5">

            <Clock className="text-orange-500 mb-3"/>

            <h3 className="font-semibold">
              Duration
            </h3>

            <p className="text-sm text-slate-500 mt-2">
              Estimated time: 30 minutes
            </p>

          </div>



          <div className="border rounded-xl p-5">

            <ShieldCheck className="text-purple-600 mb-3"/>

            <h3 className="font-semibold">
              Secure Assessment
            </h3>

            <p className="text-sm text-slate-500 mt-2">
              Your interview data is securely processed.
            </p>

          </div>


        </div>



        <button
          onClick={startInterview}  
          className="
          mt-8
          w-full
          flex
          justify-center
          items-center
          gap-3
          bg-blue-600
          hover:bg-blue-700
          text-white
          py-4
          rounded-xl
          font-semibold
          text-lg
          "
        >

          <Play size={22}/>
          Begin Interview

        </button>


      </div>

    </div>
  );
}