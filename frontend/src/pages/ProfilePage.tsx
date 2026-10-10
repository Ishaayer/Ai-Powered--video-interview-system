import { useEffect, useState } from "react";

import {
  User,
  Mail,
  Phone,
  MapPin,
  Image,
} from "lucide-react";

import PageHeader from "@/components/common/PageHeader";
import SectionCard from "@/components/common/SectionCard";
import PrimaryButton from "@/components/common/PrimaryButton";

import { authService } from "@/services/auth.service";
import { candidateProfileService } from "@/services/candidateProfile.service";

export default function ProfilePage() {

  const [loading, setLoading] = useState(true);

  const [user, setUser] = useState<any>(null);

  const [profileExists, setProfileExists] =
    useState(false);

  const [imagePreview, setImagePreview] =
    useState("");

  const [showImageModal, setShowImageModal] =
    useState(false);

  const [form, setForm] = useState({

    full_name: "",

    email: "",

    phone: "",

    location: "",

    education: "",

    experience: "",

    skills: "",

    linkedin_url: "",

    github_url: "",

  });


  const loadProfile = async () => {

    try {

      const me = await authService.me();

      setUser(me);

      setForm((prev) => ({

        ...prev,

        full_name: me.full_name,

        email: me.email,

      }));


      try {

        const profile =
          await candidateProfileService.getProfile();

        setProfileExists(true);

        setImagePreview(
          profile.profile_image || ""
        );

        setForm({

          full_name: profile.full_name,

          email: me.email,

          phone: profile.phone || "",

          location: profile.location || "",

          education: profile.education || "",

          experience: profile.experience || "",

          skills: profile.skills || "",

          linkedin_url:
            profile.linkedin_url || "",

          github_url:
            profile.github_url || "",

        });

      }

      catch (error: any) {

        console.error("Profile fetch error:", error?.response?.data || error?.message);
        setProfileExists(false);

      }

    }

    finally {

      setLoading(false);

    }

  };


  useEffect(() => {

    loadProfile();

  }, []);


  const handleChange = (

    e: React.ChangeEvent<
      HTMLInputElement |
      HTMLTextAreaElement
    >

  ) => {

    setForm({

      ...form,

      [e.target.name]:
      e.target.value,

    });

  };


  const handleImageUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file =
      e.target.files?.[0];
    if (!file) return;
    try {
      const result =
        await candidateProfileService.uploadImage(
          file
        );
      setImagePreview(
        result.profile_image
      );
      alert(
        "Profile image uploaded"
      );
    }
    catch(error: any){
      console.error("Upload error:", error);
      console.error("Error message:", error?.message);
      console.error("Error response:", error?.response?.data);
      alert(
        "Image upload failed: " + (error?.response?.data?.detail || error?.message || "Unknown error")
      );
    }
  };


  const saveProfile = async () => {

    const payload = {

      phone: form.phone,

      location: form.location,

      education: form.education,

      experience: form.experience,

      skills: form.skills,

      linkedin_url:
        form.linkedin_url,

      github_url:
        form.github_url,

    };

    try {

      if (profileExists) {

        await candidateProfileService
          .updateProfile(payload as any);

      }

      else {

        await candidateProfileService
          .createProfile(payload as any);

        setProfileExists(true);

      }

      alert("Profile saved successfully.");

    }

    catch (error: any) {

      console.error("Save error:", error);
      console.error("Error message:", error?.message);
      console.error("Error response:", error?.response?.data);

      alert("Unable to save profile: " + (error?.response?.data?.detail || error?.message || "Unknown error"));

    }

  };


  if (loading) {

    return (

      <div className="p-10">

        Loading...

      </div>

    );

  }


  return (

    <div className="space-y-8">

      <PageHeader
        title="Candidate Profile"
        subtitle="Manage your personal information and professional profile."
      />

      <div className="grid gap-8 lg:grid-cols-3">


      <SectionCard title="Profile">

        <div className="flex flex-col items-center">

          <div className="relative">
            <div 
              className="flex h-48 w-48 items-center justify-center overflow-hidden rounded-full bg-blue-100 cursor-pointer hover:opacity-80 transition-opacity"
              onClick={() => imagePreview && setShowImageModal(true)}
            >
              {
                imagePreview ? (
                  <img
                    src={`http://localhost:8000/${imagePreview}`}
                    alt="Profile"
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <User
                    size={80}
                    className="text-blue-600"
                  />
                )
              }
            </div>
            <label
              className="
                absolute
                bottom-0
                right-0
                cursor-pointer
                rounded-full
                bg-blue-600
                p-2
                text-white
                hover:bg-blue-700
                transition-colors
              "
            >
              <Image size={16}/>
              <input
                type="file"
                accept="image/*"
                hidden
                onChange={handleImageUpload}
              />
            </label>
          </div>

          <h2 className="mt-5 text-xl font-bold">
            {form.full_name}
          </h2>

          <p className="text-slate-500">
            Candidate
          </p>

          <div className="mt-6 w-full space-y-4">

            <div className="flex items-center gap-3">
              <Mail size={18} />
              <span>{form.email}</span>
            </div>

            <div className="flex items-center gap-3">
              <Phone size={18} />
              <span>{form.phone || "-"}</span>
            </div>

            <div className="flex items-center gap-3">
              <MapPin size={18} />
              <span>{form.location || "-"}</span>
            </div>

          </div>

          <div className="mt-6 flex gap-4">

            {form.linkedin_url && (
              <a
                href={form.linkedin_url}
                target="_blank"
                rel="noreferrer"
                className="text-blue-600 hover:text-blue-800"
              >
                LinkedIn
              </a>
            )}

            {form.github_url && (
              <a
                href={form.github_url}
                target="_blank"
                rel="noreferrer"
                className="text-gray-700 hover:text-black"
              >
                GitHub
              </a>
            )}

          </div>

        </div>

      </SectionCard>

      <div className="space-y-8 lg:col-span-2">

        <SectionCard title="Basic Information">

          <div className="grid gap-5 md:grid-cols-2">

            <div>
              <label className="mb-2 block font-medium">Full Name</label>
              <input
                value={form.full_name}
                disabled
                className="w-full rounded-xl border p-3 bg-slate-100"
              />
            </div>

            <div>
              <label className="mb-2 block font-medium">Email</label>
              <input
                value={form.email}
                disabled
                className="w-full rounded-xl border p-3 bg-slate-100"
              />
            </div>

            <div>
              <label className="mb-2 block font-medium">Phone</label>
              <input
                name="phone"
                value={form.phone}
                onChange={handleChange}
                className="w-full rounded-xl border p-3"
              />
            </div>

            <div>
              <label className="mb-2 block font-medium">Location</label>
              <input
                name="location"
                value={form.location}
                onChange={handleChange}
                className="w-full rounded-xl border p-3"
              />
            </div>

            <div>
              <label className="mb-2 block font-medium">LinkedIn</label>
              <input
                name="linkedin_url"
                value={form.linkedin_url}
                onChange={handleChange}
                className="w-full rounded-xl border p-3"
              />
            </div>

            <div>
              <label className="mb-2 block font-medium">GitHub</label>
              <input
                name="github_url"
                value={form.github_url}
                onChange={handleChange}
                className="w-full rounded-xl border p-3"
              />
            </div>

          </div>

        </SectionCard>

        <SectionCard title="Education">
          <textarea
            name="education"
            value={form.education}
            onChange={handleChange}
            rows={3}
            className="w-full rounded-xl border p-3"
          />
        </SectionCard>

        <SectionCard title="Experience">
          <textarea
            name="experience"
            value={form.experience}
            onChange={handleChange}
            rows={3}
            className="w-full rounded-xl border p-3"
          />
        </SectionCard>

        <SectionCard title="Skills">
          <textarea
            name="skills"
            value={form.skills}
            onChange={handleChange}
            rows={3}
            placeholder="Python, FastAPI, React, SQL"
            className="w-full rounded-xl border p-3"
          />
        </SectionCard>

        <div className="flex justify-end">

          <PrimaryButton onClick={saveProfile}>
            Save Profile
          </PrimaryButton>

        </div>

      </div>

    </div>

    {/* Image Preview Modal */}
    {showImageModal && (
      <div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 p-4"
        onClick={() => setShowImageModal(false)}
      >
        <div
          className="relative max-w-2xl max-h-96 w-full h-full flex items-center justify-center"
          onClick={(e) => e.stopPropagation()}
        >
          <img
            src={`http://localhost:8000/${imagePreview}`}
            alt="Profile Preview"
            className="w-full h-full object-contain rounded-lg"
          />
          
          {/* Close Button */}
          <button
            onClick={() => setShowImageModal(false)}
            className="absolute top-4 right-4 bg-white rounded-full p-2 hover:bg-gray-200 transition-colors"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    )}
  </div>

);

}