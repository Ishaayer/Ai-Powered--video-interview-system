import api from "./api";


export const answerService = {


  createAnswer: async (
    interviewId: string,
    questionId: number
  ) => {


    const response = await api.post(
      "/answers",
      {
        interview_id: Number(interviewId),
        question_id: questionId,
        answer_text: null,
        video_url: null,
      }
    );


    return response.data;

  },


};