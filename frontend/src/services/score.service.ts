import api from "./api";


export const scoreService = {

  getScore: async (
    interviewId: string
  ) => {

    const response = await api.get(
      `/scores/${interviewId}`
    );

    return response.data;

  },

};