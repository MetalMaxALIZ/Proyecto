import React, { useState } from 'react';
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
        setError('No se pudieron obtener los juegos');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error al conectar con el servidor. Asegúrate de que el backend esté ejecutándose.');
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
      setError('Debes seleccionar al menos un juego');
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
      } else {
        setError(response.data.error || 'No se pudieron generar recomendaciones');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error al obtener recomendaciones');
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
              placeholder="Introduce tu URL de perfil de Steam"
              className="input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading || !perfilUrl}
            >
              {loading ? 'Cargando...' : 'Obtener Juegos'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {juegos.length > 0 && (
          <>
            <GameList 
              juegos={juegos}
              juegosSeleccionados={juegosSeleccionados}
              onToggleJuego={handleToggleJuego}
            />

            <div className="wsip-section">
              <button 
                onClick={handleWSIP}
                className="btn btn-wsip"
                disabled={loadingRecomendaciones || juegosSeleccionados.length === 0}
              >
                {loadingRecomendaciones ? 'Generando...' : `WSIP (${juegosSeleccionados.length} seleccionados)`}
              </button>
            </div>
          </>
        )}

        {recomendaciones.length > 0 && (
          <Recommendations recomendaciones={recomendaciones} />
        )}
      </div>
    </div>
  );
}

export default App;
