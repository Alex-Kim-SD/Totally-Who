import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useModal } from '../../../context/Modal';
import { useHistory } from 'react-router-dom';
import './CreateBotModal.css';

function CreateBotModal() {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const [name, setName] = useState('');
  const [settings, setSettings] = useState('');
  const [errors, setErrors] = useState([]);

  const user = useSelector(state => state.session.user);

  const history = useHistory();

  const createBot = async (event) => {
    event.preventDefault();

    // Send fetch request
    const response = await fetch('/api/bots', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name,
        user_id: user.id,
        settings,
      }),
    });

    if(response.ok) {
      const bot = await response.json();
      history.push(`/bots/${bot.id}`);
      closeModal();
    } else {
      const data = await response.json();
      setErrors(data.errors);
    }
  };

  return (
    <div className="create-bot-modal">
      <h2>Create Bot</h2>
      {errors.map((error, i) => (
        <div key={i} className="error">{error}</div>
      ))}
      <form onSubmit={createBot}>
        <label>
          Bot Name:
          <input type="text" value={name} onChange={e => setName(e.target.value)} required />
        </label>
        <label>
          Bot Settings:
          <textarea value={settings} onChange={e => setSettings(e.target.value)} />
        </label>
        <div className="button-group">
          <button type="submit" className="create-button">Create Bot</button>
          <button type="button" className="cancel-button" onClick={closeModal}>Cancel</button>
        </div>
      </form>
    </div>
  );
}

export default CreateBotModal;
