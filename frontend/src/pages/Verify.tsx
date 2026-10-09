import { useParams } from 'react-router-dom';
import { ShieldAlert } from 'lucide-react';

export default function Verify() {
  const { id } = useParams();

  return (
    <div className="w-full bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center mt-12">
      <ShieldAlert className="w-16 h-16 text-amber-500 mx-auto mb-4" />
      <h1 className="text-2xl font-bold text-slate-800 mb-2">Verification Portal</h1>
      <p className="text-slate-600 mb-6">Checking document ID: <span className="font-mono bg-slate-100 px-2 py-1 rounded">{id}</span></p>
      <div className="inline-block px-4 py-2 bg-slate-50 text-slate-500 rounded border border-slate-200">
        Demo Verification Mode
      </div>
    </div>
  );
}
