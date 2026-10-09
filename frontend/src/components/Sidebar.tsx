import { Link, useLocation } from 'react-router-dom';
import { ShieldCheck, LayoutDashboard, FileText, Users } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

export default function Sidebar() {
  const location = useLocation();
  const user = useAuthStore(s => s.user);

  const links = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/documents', label: 'Documents', icon: FileText },
    ...(user?.role === 'ADMIN' ? [{ to: '/admin/users', label: 'Users', icon: Users }] : [])
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-slate-800 text-white">
        <ShieldCheck className="w-6 h-6 text-primary-500 mr-2" />
        <span className="font-bold text-lg tracking-wide">TrustDoc AI</span>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = location.pathname.startsWith(link.to);
          return (
            <Link
              key={link.to}
              to={link.to}
              className={`flex items-center px-3 py-2.5 rounded-lg transition-colors ${isActive ? 'bg-primary-600 text-white' : 'hover:bg-slate-800 hover:text-white'}`}
            >
              <Icon className="w-5 h-5 mr-3" />
              <span className="font-medium">{link.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
