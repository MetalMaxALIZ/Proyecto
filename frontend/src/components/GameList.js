import React from 'react';
import './GameList.css';

function GameList({ juegos, juegosSeleccionados, onToggleJuego }) {
  return (
    <div className="game-list-container">
      <h2 className="section-title">Tus Juegos ({juegos.length})</h2>
      <p className="section-subtitle">Selecciona los juegos en los que quieres basarte para obtener recomendaciones</p>
      
      <div className="game-grid">
        {juegos.map((juego) => {
          const isSelected = juegosSeleccionados.includes(juego.nombre);
          
          return (
            <div
              key={juego.app_id}
              className={`game-card ${isSelected ? 'selected' : ''}`}
              onClick={() => onToggleJuego(juego.nombre)}
            >
              {isSelected && (
                <div className="check-mark">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
              )}
              
              <div className="game-image-container">
                <img
                  src={juego.img_icon_url}
                  alt={juego.nombre}
                  className="game-image"
                  onError={(e) => {
                    e.target.src = `https://cdn.cloudflare.steamstatic.com/steam/apps/${juego.app_id}/header.jpg`;
                  }}
                />
              </div>
              
              <div className="game-info">
                <h3 className="game-title">{juego.nombre}</h3>
                <p className="game-playtime">
                  ⏱️ {juego.tiempo_juego_horas.toFixed(1)} horas
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default GameList;
