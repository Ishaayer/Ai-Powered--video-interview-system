import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
  loginSchema,
  type LoginFormData,
} from "@/schemas/auth.schema";

import { authService } from "@/services/auth.service";


export default function LoginPage() {

  const {
    register,
    handleSubmit,
    formState: {
      errors,
    },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });


  const onSubmit = async (
    data: LoginFormData
  ) => {

    try {

      const response =
        await authService.login(data);


      localStorage.setItem(
        "access_token",
        response.access_token
      );


      localStorage.setItem(
        "refresh_token",
        response.refresh_token
      );


      alert("Login successful");


    } catch (error) {

      console.error(
        "Login error:",
        error
      );

      alert("Login failed");

    }

  };


  return (

    <div className="
      flex
      min-h-screen
      items-center
      justify-center
    ">

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="
          w-full
          max-w-md
          space-y-5
          rounded-lg
          border
          p-8
        "
      >

        <h1 className="
          text-3xl
          font-bold
          text-center
        ">
          Login
        </h1>


        <div>

          <input
            type="email"
            placeholder="Email"

            {...register("email")}

            className="
              w-full
              rounded
              border
              p-3
            "
          />

          <p className="text-red-500">
            {errors.email?.message}
          </p>

        </div>



        <div>

          <input
            type="password"
            placeholder="Password"

            {...register("password")}

            className="
              w-full
              rounded
              border
              p-3
            "
          />

          <p className="text-red-500">
            {errors.password?.message}
          </p>

        </div>



        <button
          type="submit"
          className="
            w-full
            rounded
            bg-black
            p-3
            text-white
          "
        >
          Login
        </button>


      </form>

    </div>

  );
}