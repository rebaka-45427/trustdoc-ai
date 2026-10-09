import { useAuthStore } from '../store/authStore';

export default function Dashboard() {
  const user = useAuthStore(s => s.user);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Total Documents</h3>
          <p className="text-3xl font-bold text-slate-900">124</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Pending Review</h3>
          <p className="text-3xl font-bold text-amber-500">12</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Suspicious</h3>
          <p className="text-3xl font-bold text-red-500">3</p>
        </div>
      </div>
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">Welcome back, {user?.fullName}</h2>
        <p className="text-slate-600">You are logged in as <span className="font-semibold text-primary-600">{user?.role}</span>.</p>
      </div>
    </div>
  );
}
