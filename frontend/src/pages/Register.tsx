import { Link } from 'react-router-dom';
import { UserPlus } from 'lucide-react';

export default function Register() {
  return (
    <div>
      <div className="text-center mb-8">
        <div className="mx-auto w-12 h-12 bg-primary-100 flex items-center justify-center rounded-full mb-4">
          <UserPlus className="w-6 h-6 text-primary-600" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900">Create an Account</h2>
      </div>
      <form className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
          <input type="text" className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input type="email" className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input type="password" className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500" required />
        </div>
        <button type="button" className="w-full py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 font-medium transition-colors">
          Register
        </button>
      </form>
      <div className="mt-6 text-center text-sm">
        <span className="text-slate-500">Already have an account? </span>
        <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">Sign in</Link>
      </div>
    </div>
  );
}
