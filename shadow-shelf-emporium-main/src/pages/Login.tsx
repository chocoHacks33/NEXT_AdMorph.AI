
import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { user, login } = useAuth();

  // If user is already logged in, redirect to home
  if (user) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    const success = login(username, password);
    if (!success) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">NM</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-white">Sign in to NightMarket</h2>
          <p className="mt-2 text-gray-400">Access your account</p>
        </div>

        <div className="bg-gray-900 rounded-lg p-8 border border-gray-800">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <Label htmlFor="username" className="text-white">Username</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="mt-1 bg-gray-800 border-gray-700 text-white placeholder-gray-400"
                placeholder="Enter username"
                required
              />
            </div>

            <div>
              <Label htmlFor="password" className="text-white">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 bg-gray-800 border-gray-700 text-white placeholder-gray-400"
                placeholder="Enter password"
                required
              />
            </div>

            {error && (
              <div className="text-red-400 text-sm text-center">{error}</div>
            )}

            <Button
              type="submit"
              className="w-full bg-purple-600 hover:bg-purple-700 text-white"
            >
              Sign In
            </Button>
          </form>

          <div className="mt-6 p-4 bg-gray-800 rounded-lg">
            <h3 className="text-white font-semibold mb-2">Test Accounts:</h3>
            <div className="text-sm text-gray-300 space-y-1">
              <div>Username: a, Password: a</div>
              <div>Username: b, Password: b</div>
              <div>Username: c, Password: c</div>
              <div>Username: d, Password: d</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
