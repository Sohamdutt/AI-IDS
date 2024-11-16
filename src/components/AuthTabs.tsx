import React, { useState } from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import clsx from 'clsx';

export default function AuthTabs() {
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex mb-6 border-b">
        <button
          className={clsx(
            'flex-1 py-2 text-center',
            activeTab === 'login'
              ? 'border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          )}
          onClick={() => setActiveTab('login')}
        >
          Login
        </button>
        <button
          className={clsx(
            'flex-1 py-2 text-center',
            activeTab === 'register'
              ? 'border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          )}
          onClick={() => setActiveTab('register')}
        >
          Register
        </button>
      </div>
      {activeTab === 'login' ? <LoginForm /> : <RegisterForm />}
    </div>
  );
}