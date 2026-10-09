import { Outlet } from 'react-router-dom';

export default function PublicLayout() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center">
      <main className="w-full max-w-4xl px-4 py-8 flex-1 flex flex-col">
        <Outlet />
      </main>
    </div>
  );
}
