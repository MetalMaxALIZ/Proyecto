import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';
import GameList from './components/GameList';
import Recommendations from './components/Recommendations';

function App() {
  const [perfilUrl, setPerfilUrl] = useState('');
  const [juegos, setJuegos] = useState([]);
  const [juegosSeleccionados, setJuegosSeleccionados] = useState([]);
  const [recomendaciones, setRecomendaciones] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingRecomendaciones, setLoadingRecomendaciones] = useState(false);
  const recomendacionesRef = useRef(null);

  const handleObtenerJuegos = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setJuegos([]);
    setJuegosSeleccionados([]);
    setRecomendaciones([]);

    try {
      const response = await axios.post('/api/obtener-juegos', {
        perfil_url: perfilUrl
      });

      if (response.data.success) {
        setJuegos(response.data.juegos);
      } else {
        setError('Could not fetch games');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error connecting to server. Make sure the backend is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleJuego = (nombreJuego) => {
    setJuegosSeleccionados(prev => {
      if (prev.includes(nombreJuego)) {
        return prev.filter(j => j !== nombreJuego);
      } else {
        return [...prev, nombreJuego];
      }
    });
  };

  const handleWSIP = async () => {
    if (juegosSeleccionados.length === 0) {
      setError('You must select at least one game');
      return;
    }

    setError('');
    setLoadingRecomendaciones(true);
    setRecomendaciones([]);

    try {
      const response = await axios.post('/api/recomendar', {
        nombres_juegos: juegosSeleccionados,
        n_recomendaciones: 10
      });

      if (response.data.success) {
        setRecomendaciones(response.data.recomendaciones);
        // Scroll to recommendations after they load
        setTimeout(() => {
          recomendacionesRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
      } else {
        setError(response.data.error || 'Could not generate recommendations');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error getting recommendations');
      console.error('Error:', err);
    } finally {
      setLoadingRecomendaciones(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">What should i play?</h1>
        
        <form onSubmit={handleObtenerJuegos} className="form">
          <div className="input-group">
            <input
              type="text"
              value={perfilUrl}
              onChange={(e) => setPerfilUrl(e.target.value)}
              placeholder="Enter your Steam profile URL"
              className="input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading || !perfilUrl}
            >
              {loading ? 'Loading...' : 'Get Games'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {juegos.length > 0 && (
          <GameList 
            juegos={juegos}
            juegosSeleccionados={juegosSeleccionados}
            onToggleJuego={handleToggleJuego}
          />
        )}

        {recomendaciones.length > 0 && (
          <div ref={recomendacionesRef}>
            <Recommendations recomendaciones={recomendaciones} />
          </div>
        )}
      </div>

      {juegos.length > 0 && (
        <button 
          onClick={handleWSIP}
          className="btn btn-wsip btn-wsip-fixed"
          disabled={loadingRecomendaciones || juegosSeleccionados.length === 0}
        >
          {loadingRecomendaciones ? 'Generating...' : `WSIP (${juegosSeleccionados.length})`}
        </button>
      )}
    </div>
  );
}

export default App;
