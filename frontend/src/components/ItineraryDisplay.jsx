// frontend/src/components/ItineraryDisplay.jsx
import React from 'react';

// A simple utility component for the "Get Directions" link
const DirectionsLink = ({ from, to }) => {
  if (!from || !to) {
    return null;
  }

  // Create the Google Maps URL
  const origin = `${from.lat},${from.lon}`;
  const destination = `${to.lat},${to.lon}`;
  const mapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}`;

  return (
    <a 
      href={mapsUrl} 
      target="_blank" 
      rel="noopener noreferrer" 
      className="directions-link"
    >
      → Directions from {from.name}
    </a>
  );
};

function ItineraryDisplay({ itinerary }) {
  if (!itinerary) {
    return null;
  }

  return (
    <div className="itinerary">
      <h2>Your Personalized Itinerary</h2>
      {itinerary.map((day) => (
        <div key={day.day} className="day-card">
          <h3>Day {day.day}</h3>
          <ul>
            {day.schedule.length > 0 ? (
              day.schedule.map((item, index) => {
                // Get the previous item to create the directions link
                const prevItem = index > 0 ? day.schedule[index - 1] : null;

                return (
                  <li key={index}>
                    {/* Add the directions link if this is not the first item */}
                    {index > 0 && <DirectionsLink from={prevItem} to={item} />}
                    
                    <strong>{item.name}</strong> 
                    <span>({item.duration} hrs)</span>
                    <p>{item.description}</p>
                  </li>
                );
              })
            ) : (
              <p>No activities planned for this day. Time for a break!</p>
            )}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default ItineraryDisplay;