import api from "./api";


export const profileService = {

  getProfile: async () => {
    const response = await api.get(
      "/candidate/profile"
    );

    return response.data;
  },


  updateProfile: async (
    data: any
  ) => {

    const response = await api.put(
      "/candidate/profile",
      data
    );

    return response.data;
  },

};