import { Link } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <ShieldCheck className="w-20 h-20 text-primary-600 mb-8" />
      <h1 className="text-4xl font-bold text-slate-900 mb-4">TrustDoc AI</h1>
      <p className="text-xl text-slate-600 mb-8 text-center max-w-2xl">
        AI-powered document verification and fraud detection platform.
      </p>
      <div className="flex gap-4">
        <Link to="/login" className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700">
          Login
        </Link>
        <Link to="/register" className="px-6 py-3 bg-white text-slate-700 border border-slate-300 rounded-lg font-medium hover:bg-slate-50">
          Register
        </Link>
      </div>
    </div>
  );
}
