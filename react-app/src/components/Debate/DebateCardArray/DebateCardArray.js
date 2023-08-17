import React, { useEffect } from 'react';
import DebateCard from '../DebateCard/DebateCard';
import './DebateCardArray.css'

function DebateCardArray({ debates }) {
  if (!debates.length) {
    return <div>No debates found</div>;
  }

  return (
    <div className="card-list-container">
      {debates.map((debate) => (
        <DebateCard key={debate.id} debate={debate} />
      ))}
    </div>
  );
}


export default DebateCardArray;
