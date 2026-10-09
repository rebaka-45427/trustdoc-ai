import { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useNavigate, Link } from 'react-router-dom';
import { Lock } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('demo@trustdoc.ai');
  const [password, setPassword] = useState('password123');
  const login = useAuthStore(s => s.login);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login('mock-token', 'mock-refresh', {
      id: '1',
      email,
      fullName: 'Demo User',
      role: 'ADMIN'
    });
    navigate('/dashboard');
  };

  return (
    <div>
      <div className="text-center mb-8">
        <div className="mx-auto w-12 h-12 bg-primary-100 flex items-center justify-center rounded-full mb-4">
          <Lock className="w-6 h-6 text-primary-600" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900">Sign in to TrustDoc AI</h2>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input 
            type="email" 
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input 
            type="password" 
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            required 
          />
        </div>
        <button type="submit" className="w-full py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 font-medium transition-colors">
          Sign In
        </button>
      </form>
      <div className="mt-6 text-center text-sm">
        <span className="text-slate-500">Don't have an account? </span>
        <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">Register</Link>
      </div>
    </div>
  );
}
