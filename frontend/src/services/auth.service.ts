import api from "./api";


interface LoginPayload {
  email: string;
  password: string;
}


interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
}


export const authService = {


  register: async (
    data: RegisterPayload
  ) => {

    const response = await api.post(
      "/auth/register",
      data
    );

    return response.data;

  },


  login: async (
    data: LoginPayload
  ) => {

    const formData = new URLSearchParams();

    formData.append(
      "username",
      data.email
    );

    formData.append(
      "password",
      data.password
    );


    const response = await api.post(
      "/auth/login",
      formData,
      {
        headers: {
          "Content-Type":
          "application/x-www-form-urlencoded",
        },
      }
    );


    return response.data;

  },


  me: async () => {

    const response = await api.get(
      "/auth/me"
    );

    return response.data;

  },


};