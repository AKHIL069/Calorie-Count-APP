import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [form, setForm] = useState({ dish_name: '', servings: 1 });
  const [result, setResult] = useState(null);
  const [meals, setMeals] = useState([]);

  const token = localStorage.getItem('token');

  const fetchMeals = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/meals', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMeals(res.data);
    } catch (err) {
      console.error('Failed to load meals');
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('https://calorie-count-app-backend.onrender.com/api/get-calories', form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setResult(res.data);
      fetchMeals();
    } catch (err) {
      alert(err.response?.data?.detail || 'Request failed');
    }
  };

  useEffect(() => {
    fetchMeals();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Calorie Checker</h2>
      <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
        <input
          name="dish_name"
          placeholder="Dish name"
          className="p-2 border rounded"
          value={form.dish_name}
          onChange={handleChange}
        />
        <input
          name="servings"
          type="number"
          placeholder="Servings"
          className="p-2 border rounded"
          value={form.servings}
          onChange={handleChange}
        />
        <button type="submit" className="bg-green-600 text-white px-4 rounded">Search</button>
      </form>

      {result && (
        <div className="bg-white p-4 rounded shadow mb-4">
          <h3 className="font-bold">{result.dish_name}</h3>
          <p>Total Calories: {result.total_calories}</p>
          <p>Calories per Serving: {result.calories_per_serving}</p>
          <p>Protein: {result.macronutrients.protein_g}g</p>
          <p>Fat: {result.macronutrients.fat_g}g</p>
          <p>Carbs: {result.macronutrients.carbs_g}g</p>
        </div>
      )}

      <h3 className="text-xl font-semibold mt-6 mb-2">Meal History</h3>
      <ul className="list-disc pl-5">
        {meals.map((meal) => (
          <li key={meal.id}>
            {meal.dish_name} – {meal.total_calories} kcal on {new Date(meal.created_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;