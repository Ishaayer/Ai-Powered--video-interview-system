import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  User,
  FileText,
  ClipboardList,
  BarChart3,
} from "lucide-react";

const menu = [
  {
    name: "Dashboard",
    path: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Profile",
    path: "/profile",
    icon: User,
  },
  {
    name: "Resume",
    path: "/resume",
    icon: FileText,
  },
  {
    name: "Interviews",
    path: "/interviews",
    icon: ClipboardList,
  },
  {
    name: "Reports",
    path: "/reports",
    icon: BarChart3,
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white flex flex-col">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold">
          AI Interview
        </h1>
      </div>

      <nav className="flex-1 flex flex-col gap-2 p-4">
        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-4 py-3 transition ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <Icon size={20} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}