// frontend/src/components/ItineraryForm.jsx
import React, { useState } from 'react';

function ItineraryForm({ onGenerate, isLoading }) {
  const [interests, setInterests] = useState('');
  const [duration, setDuration] = useState(2); // Default to 2 days

  const handleSubmit = (e) => {
    e.preventDefault();
    // Filter out empty strings that might result from trailing commas
    const interestsArray = interests
      .split(',')
      .map(item => item.trim())
      .filter(item => item); // This removes empty strings
    
    onGenerate({ interests: interestsArray, duration: parseInt(duration) });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="interests">Interests (comma-separated)</label>
        <input
          id="interests"
          type="text"
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          placeholder="e.g., history, food, sea"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="duration">Duration (days)</label>
        <input
          id="duration"
          type="number"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          min="1"
          max="7"
          required
        />
      </div>
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Generating Plan...' : '✨ Generate My Itinerary'}
      </button>
    </form>
  );
}

export default ItineraryForm;