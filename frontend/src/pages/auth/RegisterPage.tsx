import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";


import {
  registerSchema,
  type RegisterFormData
} from "@/schemas/auth.schema";


import {
  authService
} from "@/services/auth.service";



export default function RegisterPage(){


const {

 register,

 handleSubmit,

 formState:{
  errors
 }

}=useForm<RegisterFormData>({

 resolver:zodResolver(registerSchema)

});



const onSubmit = async(
 data:RegisterFormData
)=>{

 try{

  await authService.register(data);


  alert(
    "Registration successful"
  );


 }catch(error){

  console.error(error);


  alert(
    "Registration failed"
  );

 }

};



return(

<div className="
 flex
 min-h-screen
 items-center
 justify-center
">


<form

onSubmit={
 handleSubmit(onSubmit)
}

className="
 w-full
 max-w-md
 space-y-5
 rounded-lg
 border
 p-8
 shadow
"


>


<h1 className="
text-3xl
font-bold
text-center
">

Register

</h1>



<input

{...register("full_name")}

placeholder="Full Name"

className="
w-full
rounded
border
p-3
"

/>


<p className="text-red-500">
{
errors.full_name?.message
}
</p>




<input

{...register("email")}

placeholder="Email"

className="
w-full
rounded
border
p-3
"

/>


<p className="text-red-500">
{
errors.email?.message
}
</p>




<input

type="password"

{...register("password")}

placeholder="Password"

className="
w-full
rounded
border
p-3
"

/>


<p className="text-red-500">
{
errors.password?.message
}
</p>



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

Register

</button>


</form>


</div>

);


}