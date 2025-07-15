import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/auth/register', form);
      alert('Registration successful. Please login.');
      window.location.href = '/login';
    } catch (err) {
      alert(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form className="bg-white p-6 rounded shadow-md w-80" onSubmit={handleSubmit}>
        <h2 className="text-xl font-bold mb-4">Register</h2>
        {['first_name', 'last_name', 'email', 'password'].map((field) => (
          <input
            key={field}
            name={field}
            type={field === 'password' ? 'password' : 'text'}
            placeholder={field.replace('_', ' ')}
            className="mb-2 p-2 w-full border rounded"
            value={form[field]}
            onChange={handleChange}
          />
        ))}
        <button type="submit" className="bg-blue-500 text-white py-2 w-full rounded">Register</button>
      </form>
    </div>
  );
};

export default Register;