import api from "./api";


const resumeService = {


  uploadResume: async (file: File) => {

    const formData = new FormData();

    formData.append("file", file);


    console.log("Sending file:", file);


    const response = await api.post(
      "/resume/upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );


    return response.data;

  },



  getResume: async () => {

    const response = await api.get("/resume");

    return response.data;

  },



  deleteResume: async () => {

    const response = await api.delete("/resume");

    return response.data;

  }


};


export default resumeService;