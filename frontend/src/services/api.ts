import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {},
  timeout: 15000, // 15 second timeout
});

// ===== REQUEST INTERCEPTOR =====
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    console.error("Request Error:", error);
    return Promise.reject(error);
  }
);

// ===== RESPONSE INTERCEPTOR =====
api.interceptors.response.use(
  (response) => {
    // Return response as is (don't change format)
    return response;
  },
  (error) => {
    const status = error.response?.status;
    const errorMessage =
      error.response?.data?.message ||
      error.message ||
      "An error occurred";

    console.error(`API Error [${status}]:`, errorMessage);

    // Handle specific status codes
    switch (status) {
      case 400:
        console.error("Bad Request:", errorMessage);
        break;

      case 401:
        // Unauthorized - clear tokens and redirect to login
        console.error("Unauthorized - Clearing tokens");
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        // Redirect to login after a short delay
        setTimeout(() => {
          window.location.href = "/login";
        }, 500);
        break;

      case 403:
        console.error("Access Forbidden:", errorMessage);
        break;

      case 404:
        console.error("Resource Not Found:", errorMessage);
        break;

      case 500:
        console.error("Server Error:", errorMessage);
        break;

      case 502:
      case 503:
        console.error("Service Unavailable:", errorMessage);
        break;

      default:
        if (error.message === "Network Error") {
          console.error("Network Error - Check your connection");
        }
    }

    // Always reject and let services handle it
    return Promise.reject(error);
  }
);

export default api;