// frontend/src/pages/ResumePage.tsx

import { useEffect, useState } from "react";
import resumeService from "@/services/resume.service";


interface Resume {
  id: number;
  candidate_id: number;
  file_name: string;
  file_url: string;
  file_type: string;
  file_size: number;
  raw_text: string;
  parsed_skills: string;
  parsed_languages: string;
  parsed_projects: string;
  parsed_experience: string;
  uploaded_at: string;
  updated_at: string;
}


const ResumePage = () => {

  const [resume, setResume] = useState<Resume | null>(null);

  const [file, setFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(true);

  const [uploading, setUploading] = useState(false);


  // Load resume when page opens
  useEffect(() => {

    loadResume();

  }, []);



  const loadResume = async () => {

    try {

      const data = await resumeService.getResume();

      setResume(data);

    }
    catch(error){

      console.log("No resume uploaded");

      setResume(null);

    }
    finally{

      setLoading(false);

    }

  };




  // Upload Resume

  const handleUpload = async () => {


    if(!file){

      alert("Please select a resume file");

      return;

    }


    try {

      setUploading(true);


      const data = await resumeService.uploadResume(file);


      setResume(data);


      setFile(null);


    }
    catch(error){

      console.log(error);

      alert("Resume upload failed");

    }
    finally{

      setUploading(false);

    }

  };





  // Delete Resume

  const handleDelete = async()=>{


    try{


      await resumeService.deleteResume();


      setResume(null);


    }
    catch(error){

      console.log(error);

      alert("Delete failed");

    }


  };






  if(loading){

    return (

      <div className="p-6">

        Loading resume...

      </div>

    );

  }





  return (

    <div className="p-6 max-w-4xl mx-auto">


      <h1 className="text-3xl font-bold mb-6">

        Resume Management

      </h1>





      {/* Upload Section */}

      <div className="border rounded-lg p-5 mb-6">


        <h2 className="text-xl font-semibold mb-3">

          Upload Resume

        </h2>



        <input

          type="file"

          accept=".pdf,.doc,.docx"

          onChange={(e)=>

            setFile(e.target.files?.[0] || null)

          }

          className="mb-3"

        />



        <button

          onClick={handleUpload}

          disabled={uploading}

          className="bg-blue-600 text-white px-5 py-2 rounded"

        >

          {uploading ? "Uploading..." : "Upload"}

        </button>


      </div>







      {/* Resume Details */}

      {

      resume && (

        <div className="border rounded-lg p-6">


          <div className="flex justify-between items-center">


            <h2 className="text-xl font-bold">

              {resume.file_name}

            </h2>



            <button

              onClick={handleDelete}

              className="bg-red-600 text-white px-4 py-2 rounded"

            >

              Delete

            </button>


          </div>





          <div className="mt-5 space-y-4">



            <div>

              <h3 className="font-semibold">

                File Type

              </h3>

              <p>{resume.file_type}</p>

            </div>





            <div>

              <h3 className="font-semibold">

                Uploaded Date

              </h3>


              <p>

              {new Date(resume.uploaded_at).toLocaleDateString()}

              </p>


            </div>







            <div>

              <h3 className="font-semibold">

                Skills

              </h3>


              <p>

              {resume.parsed_skills || "Not extracted"}

              </p>


            </div>






            <div>

              <h3 className="font-semibold">

                Languages

              </h3>


              <p>

              {resume.parsed_languages || "Not extracted"}

              </p>


            </div>







            <div>

              <h3 className="font-semibold">

                Projects

              </h3>


              <p>

              {resume.parsed_projects || "Not extracted"}

              </p>


            </div>







            <div>

              <h3 className="font-semibold">

                Experience

              </h3>


              <p>

              {resume.parsed_experience || "Not extracted"}

              </p>


            </div>






          </div>



        </div>


      )

      }





      {

      !resume && (

        <div className="border rounded-lg p-6 text-gray-500">

          No resume uploaded yet.

        </div>

      )

      }





    </div>

  );

};


export default ResumePage;