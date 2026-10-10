import api from "./api";


export const candidateProfileService = {


  getProfile: async () => {

    const response = await api.get(
      "/candidate-profile"
    );

    return response.data;

  },


  createProfile: async (
    data: any
  ) => {

    const response = await api.post(
      "/candidate-profile",
      data
    );

    return response.data;

  },


  updateProfile: async (
    data: any
  ) => {

    const response = await api.put(
      "/candidate-profile",
      data
    );

    return response.data;

  },


  uploadImage: async (
    file: File
  ) => {

    const formData = new FormData();

    formData.append(
      "file",
      file
    );


    const response = await api.post(
      "/upload/profile-image",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      }
    );


    return response.data;

  },


};