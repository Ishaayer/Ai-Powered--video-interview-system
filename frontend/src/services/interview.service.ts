import api from "./api";


export const interviewService = {

  startInterview: async (
    topic: string,
    difficulty: string
  ) => {

    const response = await api.post(
        "/interviews/start",
        {
        topic,
        difficulty,
        }
    );

    return response.data;

},


  getInterviews: async () => {

    const response = await api.get(
      "/interviews"
    );

    return response.data;

  },


  getInterview: async (
    interviewId: string
  ) => {

    const response = await api.get(
      `/interviews/${interviewId}`
    );

    return response.data;

  },


  completeInterview: async (
    interviewId: string
  ) => {

    const response = await api.put(
      `/interviews/${interviewId}/complete`
    );

    return response.data;

  },

};