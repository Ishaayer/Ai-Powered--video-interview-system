import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { answerService } from "@/services/answer.service";
import { videoService } from "@/services/video.service";
import { questionService } from "@/services/question.service";
import { ttsService } from "@/services/tts.service";
import { interviewService } from "@/services/interview.service";
import {
  Video,
  Mic,
  Clock,
  Play,
  Volume2,
} from "lucide-react";

export default function InterviewSessionPage() {

  const { id } = useParams();
  const navigate = useNavigate();

  const videoRef = useRef<HTMLVideoElement>(null);

  const streamRef = useRef<MediaStream | null>(null);

  const [cameraReady, setCameraReady] = useState(false);

  const [micReady, setMicReady] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const chunksRef = useRef<Blob[]>([]);

  const [isRecording, setIsRecording] = useState(false);

  const [recordedBlob, setRecordedBlob] = useState<Blob | null>(null);

  const [seconds, setSeconds] = useState(0);

  const [isUploading, setIsUploading] = useState(false);

  const [questions, setQuestions] = useState<any[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);  

  const [answerId, setAnswerId] = useState<number | null>(null);

  const recordingQuestionIndexRef = useRef<number>(0);

  const speakQuestion = async () => {
  
    if (
      questions.length === 0 ||
      !questions[currentQuestionIndex]
    ) return;


    const text =
      questions[currentQuestionIndex]
        .question_text;


    console.log(
      "AI speaking:",
      text
    );


    await ttsService.speak(text);


    console.log(
      "Question finished speaking"
    );


    setTimeout(() => {

      startRecording();

    }, 1000);

  };

  useEffect(() => {

  const startCamera = async () => {

    try {

      const stream = await navigator.mediaDevices.getUserMedia({

        video: true,

        audio: true,

      });

      streamRef.current = stream;

      if (videoRef.current) {

        videoRef.current.srcObject = stream;

      }

      setCameraReady(true);

      setMicReady(true);

    } catch (error) {

      console.error(error);

      alert("Camera or microphone permission denied.");

    }

  };

  startCamera();

  return () => {

    streamRef.current?.getTracks().forEach(track => track.stop());

  };

}, []);


  useEffect(() => {
    if (!id) return;

    const loadQuestions = async () => {
      try {
        const data = await questionService.getQuestions(id);

        console.log("Questions:", data);

        setQuestions(data);

        if (data.length > 0) {
          setTimeout(async () => {
            await ttsService.speak(
              data[0].question_text
            );

            console.log("Question finished speaking");

            startRecording();

          }, 500);
        }

      } catch (error) {
        console.error(error);
        alert("Unable to load interview questions.");
      }
    };

    loadQuestions();
  }, [id]);


  useEffect(() => {

    let interval: number;

    if (isRecording) {

      interval = window.setInterval(() => {

        setSeconds(prev => prev + 1);

      }, 1000);

    }

    return () => {

      clearInterval(interval);

    };

  }, [isRecording]);


  const startRecording = () => {

  if (!streamRef.current) return;

  // Store the current question index at time of recording start
  recordingQuestionIndexRef.current = currentQuestionIndex;

  chunksRef.current = [];

  const recorder = new MediaRecorder(streamRef.current, {

    mimeType: "video/webm",

  });

  mediaRecorderRef.current = recorder;

  recorder.ondataavailable = (event) => {

    if (event.data.size > 0) {

      chunksRef.current.push(event.data);

    }

  };

  recorder.onstop = async () => {

    console.log("1. Recorder stopped");

    const blob = new Blob(chunksRef.current, {
      type: "video/webm",
    });

    console.log("2. Blob created");

    setRecordedBlob(blob);

    if (!id) return;

    try {

      const currentQuestion =
        questions[recordingQuestionIndexRef.current];

      if (!currentQuestion) {
        alert("No question found.");
        return;
      }

      console.log("3. Current question:", currentQuestion);

      const answer = await answerService.createAnswer(
        id,
        currentQuestion.id
      );

      console.log("4. Answer created:", answer);

      setAnswerId(answer.id);

      await videoService.uploadVideo(
        answer.id,
        blob
      );

      console.log("5. Video uploaded");

      await interviewService.completeInterview(id);

      console.log("6. Interview completed");

      ttsService.stop();

      streamRef.current?.getTracks().forEach(track => track.stop());

      console.log("7. Navigating");

      navigate("/dashboard");

    } catch (error) {

      console.error("Interview flow error:", error);

      alert("Unable to upload answer");

    }

  };

  recorder.start();

  setSeconds(0);

  setIsRecording(true);

};

  const stopRecording = () => {

  mediaRecorderRef.current?.stop();

  setIsRecording(false);

};

useEffect(() => {
  return () => {
    ttsService.stop();
    streamRef.current?.getTracks().forEach(track => track.stop());
  };
}, []);

  return (

    <div className="space-y-8">


      <div>

        <h1 className="text-3xl font-bold">
          Interview Session
        </h1>

        <p className="text-slate-500 mt-2">
          AI powered interview assessment
        </p>

      </div>



      <div className="grid lg:grid-cols-3 gap-6">


        {/* Camera Area */}

        <div
          className="
            lg:col-span-2
            bg-black
            rounded-2xl
            overflow-hidden
            h-[420px]
            relative
          "
        >

          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="
              w-full
              h-full
              object-cover
            "
          />

          {!cameraReady && (

            <div
              className="
                absolute
                inset-0
                flex
                items-center
                justify-center
                text-white
              "
            >

              <div className="text-center">

                <Video
                  size={50}
                  className="mx-auto mb-4"
                />

                <p>

                  Starting Camera...

                </p>

              </div>

            </div>

          )}

        </div>



        {/* Status Panel */}

        <div className="
          bg-white
          border
          rounded-2xl
          p-6
          space-y-5
        ">


          <div>

            <h2 className="text-xl font-semibold">
              Current Question
            </h2>

            <p className="mt-3 text-slate-600">
              {questions.length > 0
                ? questions[currentQuestionIndex].question_text
                : "Loading question..."}
            </p>

          </div>



          <button
            onClick={speakQuestion}
            className="
              w-full
              py-2
              px-3
              rounded-lg
              flex
              justify-center
              items-center
              gap-2
              text-slate-700
              bg-slate-100
              hover:bg-slate-200
              font-medium
              transition-colors
            "
          >
            <Volume2 size={18} />
            Repeat Question
          </button>



          <div className="flex items-center gap-3">

            <Mic className="text-green-600"/>

            <span>

            {micReady ? "Microphone Ready" : "Waiting for Permission..."}

            </span>

          </div>



          <div className="flex items-center gap-3">

            <Clock className="text-orange-500"/>

            <span>

            Recording Time : {seconds}s

            </span>             

          </div>



          <button
            onClick={
              isRecording
                ? stopRecording
                : startRecording
            }
            className={`
              w-full
              py-3
              rounded-xl
              flex
              justify-center
              items-center
              gap-2
              text-white
              font-semibold
              ${
                isRecording
                  ? "bg-red-600 hover:bg-red-700"
                  : "bg-blue-600 hover:bg-blue-700"
              }
            `}
          >

            <Play size={20}/>

            {isRecording
              ? "Stop Recording"
              : "Start Recording"}

          </button>

          {recordedBlob && (

            <div className="rounded-lg bg-green-100 p-4">

              <p className="font-semibold text-green-700">

                Recording Finished

              </p>

              <p className="text-sm text-green-600 mt-1">

                Video Size :

                {(recordedBlob.size / 1024 / 1024).toFixed(2)} MB

              </p>

            </div>

          )}         

        {isUploading && (

          <div className="rounded-lg bg-blue-100 p-4">

            <p className="font-semibold text-blue-700">

              Uploading answer...

            </p>

          </div>

        )}

        </div>


      </div>


    </div>

  );

}