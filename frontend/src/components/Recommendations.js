import React from 'react';
import './Recommendations.css';

function Recommendations({ recomendaciones }) {
  return (
    <div className="recommendations-container">
      <h2 className="recommendations-title">🎮 Recommendations for you</h2>
      
      <div className="recommendations-grid">
        {recomendaciones.map((juego, index) => (
          <div key={juego.appid} className="recommendation-card">
            <div className="recommendation-rank">#{index + 1}</div>
            
            <div className="recommendation-image-container">
              <img
                src={juego.imagen_url}
                alt={juego.name}
                className="recommendation-image"
                onError={(e) => {
                  e.target.src = `https://via.placeholder.com/460x215?text=${encodeURIComponent(juego.name)}`;
                }}
              />
            </div>
            
            <div className="recommendation-info">
              <h3 className="recommendation-name">{juego.name}</h3>
              
              <div className="recommendation-stats">
                <div className="stat-item">
                  <span className="stat-label">Genres:</span>
                  <span className="stat-value">{juego.genres || 'N/A'}</span>
                </div>
                
                <div className="stat-item">
                  <span className="stat-label">Owners:</span>
                  <span className="stat-value">{juego.owners ? juego.owners.toLocaleString() : 'N/A'}</span>
                </div>
                
                <div className="stat-item">
                  <span className="stat-label">Rating:</span>
                  <span className="stat-value">{juego.porcentaje_votos_positivos ? `${juego.porcentaje_votos_positivos}%` : 'N/A'}</span>
                </div>
                
                <div className="stat-item">
                  <span className="stat-label">Similarity:</span>
                  <div className="similarity-bar">
                    <div 
                      className="similarity-fill"
                      style={{ width: `${(juego.similitud * 100).toFixed(0)}%` }}
                    />
                  </div>
                  <span className="stat-value">{(juego.similitud * 100).toFixed(1)}%</span>
                </div>
              </div>
              
              <a
                href={`https://store.steampowered.com/app/${juego.appid}`}
                target="_blank"
                rel="noopener noreferrer"
                className="steam-link"
              >
                View on Steam →
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recommendations;
