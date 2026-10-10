import api from "./api";


export const questionService = {

  getQuestions: async (
    interviewId: string
  ) => {

    const response = await api.get(
      `/questions/interview/${interviewId}`
    );

    return response.data;

  },

};