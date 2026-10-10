import { Routes, Route } from "react-router-dom";

import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/auth/LoginPage";
import RegisterPage from "@/pages/auth/RegisterPage";

import DashboardPage from "@/pages/DashboardPage";
import ProfilePage from "@/pages/ProfilePage";
import ResumePage from "@/pages/ResumePage";

import CandidateLayout from "@/layouts/CandidateLayout";

import ProtectedRoute from "@/components/common/ProtectedRoute";

import ReportsPage from "@/pages/ReportsPage";


import InterviewsPage from "@/pages/InterviewsPage";
import StartInterviewPage from "@/pages/StartInterviewPage";
import InterviewDetailsPage from "@/pages/InterviewDetailsPage";
import InterviewSessionPage from "@/pages/InterviewSessionPage";

import NotFoundPage from "@/pages/NotFoundPage";

export function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />

      <Route path="/login" element={<LoginPage />} />

      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<CandidateLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />

          <Route path="/profile" element={<ProfilePage />} />

          <Route path="/resume" element={<ResumePage />} />

          <Route path="/interviews" element={<InterviewsPage />} />

          <Route path="/start-interview" element={<StartInterviewPage />} />

          <Route path="/interviews/:id" element={<InterviewDetailsPage />} />

          <Route path="/interviews/:id/session" element={<InterviewSessionPage />} />

          <Route path="/reports" element={<ReportsPage />} />

          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Route>
    </Routes>
  );
}