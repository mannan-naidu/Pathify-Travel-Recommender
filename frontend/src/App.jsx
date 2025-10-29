// frontend/src/App.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ItineraryForm from './components/ItineraryForm';
import ItineraryDisplay from './components/ItineraryDisplay';
import './App.css';

const API_URL = 'http://127.0.0.1:5001';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [itinerary, setItinerary] = useState(null);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  const pollTaskStatus = (id) => {
    intervalRef.current = setInterval(async () => {
      try {
        const response = await axios.get(`${API_URL}/itinerary/result/${id}`);
        if (response.data.status === 'SUCCESS') {
          setItinerary(response.data.itinerary);
          setIsLoading(false);
          setTaskId(null);
          clearInterval(intervalRef.current);
        } else if (response.data.status === 'FAILURE') {
          setError('Failed to generate itinerary. Please try different interests.');
          setIsLoading(false);
          setTaskId(null);
          clearInterval(intervalRef.current);
        }
      } catch (err) {
        setError('An error occurred while fetching results.');
        setIsLoading(false);
        clearInterval(intervalRef.current);
      }
    }, 3000); // Poll every 3 seconds
  };

  const handleGenerate = async (formData) => {
    setIsLoading(true);
    setItinerary(null);
    setError(null);
    if (intervalRef.current) clearInterval(intervalRef.current);

    try {
      const response = await axios.post(`${API_URL}/itinerary`, formData);
      setTaskId(response.data.task_id);
      pollTaskStatus(response.data.task_id);
    } catch (err) {
      setError('Failed to start itinerary generation.');
      setIsLoading(false);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);


  return (
    <div className="App">
      <header className="App-header">
        <h1>Travel Itinerary Recommender 🗺️</h1>
        <p>Enter your interests and trip duration to get a personalized travel plan.</p>
      </header>
      <main>
        <ItineraryForm onGenerate={handleGenerate} isLoading={isLoading} />
        {isLoading && <div className="loading">Generating your adventure... Please wait.</div>}
        {error && <div className="error">{error}</div>}
        {itinerary && <ItineraryDisplay itinerary={itinerary} />}
      </main>
    </div>
  );
}

export default App;