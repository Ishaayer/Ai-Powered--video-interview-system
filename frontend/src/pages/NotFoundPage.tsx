import { Link } from "react-router-dom";
import { TriangleAlert } from "lucide-react";

export default function NotFoundPage() {

  return (

    <div className="min-h-screen flex items-center justify-center bg-slate-50">

      <div className="bg-white border rounded-2xl shadow-lg p-10 text-center max-w-md">

        <TriangleAlert
          size={60}
          className="mx-auto text-red-500 mb-5"
        />

        <h1 className="text-4xl font-bold">
          404
        </h1>

        <p className="text-slate-500 mt-3">
          The page you are looking for does not exist.
        </p>

        <Link
          to="/dashboard"
          className="
            inline-block
            mt-8
            bg-blue-600
            hover:bg-blue-700
            text-white
            px-6
            py-3
            rounded-xl
            font-semibold
          "
        >
          Back to Dashboard
        </Link>

      </div>

    </div>

  );

}