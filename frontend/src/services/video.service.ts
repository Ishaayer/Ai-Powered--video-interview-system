import api from "./api";


export const videoService = {

  uploadVideo: async (
    answerId: number,
    videoBlob: Blob
  ) => {

    const formData = new FormData();


    formData.append(
      "file",
      videoBlob,
      "answer.webm"
    );


    const response = await api.post(
      `/upload/video/${answerId}`,
      formData
    );


    return response.data;

  },

};