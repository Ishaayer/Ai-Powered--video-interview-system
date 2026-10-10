import { useEffect, useState } from "react";
import { User, LogOut, Settings } from "lucide-react";
import { candidateProfileService } from "@/services/candidateProfile.service";
import { authService } from "@/services/auth.service";

export default function Navbar() {
  const [profileImage, setProfileImage] = useState("");
  const [fullName, setFullName] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      const user = await authService.me();
      setFullName(user.full_name || "");
      console.log("User loaded:", user.full_name);

      try {
        const profile = await candidateProfileService.getProfile();
        console.log("Profile image path:", profile.profile_image);
        setProfileImage(profile.profile_image || "");
      } catch {
        console.log("No profile found");
        setProfileImage("");
      }
    } catch (error) {
      console.error("Error loading profile:", error);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      window.location.href = "/login";
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6">
      <h1 className="text-xl font-bold">
        AI Interview Assessment System
      </h1>
      
      <div className="flex items-center gap-8">
        {/* User Name */}
        <div className="text-sm text-gray-600">
          {fullName || "Candidate"}
        </div>

        {/* Avatar Dropdown */}
        <div className="relative">
          {/* Avatar Button */}
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="h-12 w-12 rounded-full bg-blue-100 hover:bg-blue-200 flex items-center justify-center overflow-hidden transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {profileImage ? (
              <img
                src={`http://localhost:8000/${profileImage}`}
                alt={fullName}
                className="h-full w-full object-cover"
              />
            ) : (
              <User size={20} className="text-blue-600" />
            )}
          </button>

          {/* Dropdown Menu */}
          {showDropdown && (
            <>
              {/* Backdrop */}
              <div
                className="fixed inset-0 z-30"
                onClick={() => setShowDropdown(false)}
              />

              {/* Menu */}
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-40">
                <div className="px-4 py-3 border-b">
                  <p className="text-sm font-medium text-gray-900">
                    {fullName || "Candidate"}
                  </p>
                  <p className="text-xs text-gray-500">Candidate</p>
                </div>

                <a
                  href="/profile"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                  onClick={() => setShowDropdown(false)}
                >
                  <User size={16} />
                  View Profile
                </a>

                <a
                  href="/settings"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                  onClick={() => setShowDropdown(false)}
                >
                  <Settings size={16} />
                  Settings
                </a>

                <button
                  onClick={() => {
                    setShowDropdown(false);
                    handleLogout();
                  }}
                  className="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 border-t text-left flex items-center gap-2"
                >
                  <LogOut size={16} />
                  Logout
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}