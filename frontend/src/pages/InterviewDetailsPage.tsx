import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { interviewService } from "@/services/interview.service";
import { questionService } from "@/services/question.service";
import type { Interview } from "@/types/interview";
import type { Question } from "@/types/question";

export default function InterviewDetailsPage() {

  const { id } = useParams();

  const navigate = useNavigate();

  const [interview, setInterview] = useState<Interview | null>(null);

  const [questions, setQuestions] = useState<Question[]>([]);


  useEffect(() => {

    const loadInterview = async () => {

      if (!id) return;

      try {

        const data =
            await interviewService.getInterview(id);

        setInterview(data);


        const questionData =
            await questionService.getQuestions(id);

        setQuestions(questionData);

      } catch (error) {

        console.error(error);

      }

    };


    loadInterview();

  }, [id]);



  if (!interview) {

    return (
      <div className="p-8">
        Loading...
      </div>
    );

  }


  return (

    <div className="space-y-6">

      <h1 className="text-3xl font-bold">
        Interview Details
      </h1>


      <div className="bg-white border rounded-xl p-6 space-y-5">


        <div>
          <p className="font-semibold">
            Topic
          </p>

          <p>
            {interview.topic}
          </p>
        </div>


        <div>
          <p className="font-semibold">
            Difficulty
          </p>

          <p>
            {interview.difficulty}
          </p>
        </div>


        <div>
          <p className="font-semibold">
            Status
          </p>

          <p>
            {interview.status}
          </p>
        </div>


        <div>
          <p className="font-semibold">
            Created At
          </p>

          <p>
            {new Date(
              interview.created_at
            ).toLocaleString()}
          </p>
        </div>


        <div>
          <p className="font-semibold">
            Started At
          </p>

          <p>
            {
              interview.started_at
                ? new Date(
                    interview.started_at
                  ).toLocaleString()
                : "Not started"
            }
          </p>
        </div>


        <div>
          <p className="font-semibold">
            Completed At
          </p>

          <p>
            {
              interview.completed_at
                ? new Date(
                    interview.completed_at
                  ).toLocaleString()
                : "Not completed"
            }
          </p>
        </div>


      </div>

        <div className="bg-white border rounded-xl p-6 space-y-4">

          <h2 className="text-2xl font-bold">
              Interview Questions
          </h2>


        {
            questions.length === 0 ? (

            <p className="text-slate-500">
                No questions available.
            </p>

            ) : (

            questions.map((question, index) => (

                <div
                key={question.id}
                className="border rounded-lg p-4"
                >

                <p className="font-semibold">
                    Question {index + 1}
                </p>

                <p className="mt-2 text-slate-600">
                    {question.question_text}
                </p>

        </div>

      ))

    )
  }


</div>


{interview.status.toLowerCase() === "completed" ? (

  <button
    onClick={() => navigate("/reports")}
    className="
      w-full
      mt-6
      bg-green-600
      hover:bg-green-700
      text-white
      py-3
      rounded-xl
      font-semibold
    "
  >
    View Report
  </button>

) : (

  <button
    disabled
    className="
      w-full
      mt-6
      bg-gray-300
      text-gray-600
      py-3
      rounded-xl
      font-semibold
      cursor-not-allowed
    "
  >
    Interview In Progress
  </button>

)}


    </div>

  );

}