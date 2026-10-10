import api from "./api";

export const reportService = {

  getReport: async (
    interviewId: string
  ) => {

    const response = await api.get(
      `/reports/${interviewId}`
    );

    return response.data;

  },

};