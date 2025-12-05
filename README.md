# What Should I Play? 🎮

Steam game recommendation system with React frontend and Flask backend.

## Project Structure

```
Proyecto_con_FrontEnd/
├── backend/                 # Flask server
│   ├── app.py              # Main API
│   ├── export_model.py     # Script to export model
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameList.js
│   │   │   ├── GameList.css
│   │   │   ├── Recommendations.js
│   │   │   └── Recommendations.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── data/                   # Model data (auto-generated)
└── steam_profile_games.py  # Functions to get Steam games
```

## Initial Setup

### 1. Prepare the Recommendation Model

Before running the application, you need to export the model from the notebook:

1. Open the `pruebas.ipynb` notebook
2. Run all cells until you have the following variables:
   - `df_combinado_final`
   - `df_modelo`
   - `df_modelo_normalizado`
   - `knn_modelo`
   - `juegos_dict`

3. At the end of the notebook, run:

```python
# Import export function
import sys
sys.path.append('./backend')
from export_model import guardar_modelo

# Save the model
guardar_modelo(df_combinado_final, df_modelo, df_modelo_normalizado, knn_modelo, juegos_dict)
```

This will create the `data/` folder with all necessary files.

### 2. Configure Backend (Flask)

1. Navigate to backend folder:
```powershell
cd backend
```

2. Create a virtual environment (optional but recommended):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Start Flask server:
```powershell
python app.py
```

Server will be running at `http://localhost:5000`

### 3. Configure Frontend (React)

1. Open a new terminal and navigate to frontend folder:
```powershell
cd frontend
```

2. Install Node.js dependencies:
```powershell
npm install
```

3. Start React application:
```powershell
npm start
```

The application will automatically open at `http://localhost:3000`

## Application Usage

1. **Enter your Steam profile URL** in the text field:
   - Example: `https://steamcommunity.com/id/YourName/`
   - Or: `https://steamcommunity.com/profiles/76561198XXXXXXXXX/`

2. **Click "Get Games"** to load your library

3. **Select the games** you want to base recommendations on (click on the cards)

4. **Click the "WSIP" button** to get personalized recommendations

5. **Explore recommendations** with detailed information for each game

## Features

- ✅ Automatic game retrieval from public Steam profiles
- ✅ Game visualization with images and playtime
- ✅ Multiple game selection with intuitive interface
- ✅ KNN-based recommendation system (K-Nearest Neighbors)
- ✅ Detailed recommendation information (genres, ratings, similarity)
- ✅ Direct links to Steam store
- ✅ Responsive and modern design

## Important Notes

- **Public Profile**: Your Steam profile must be public for the app to access your library
- **API Key**: Steam API key is included in the code, but you can use your own in `backend/app.py`
- **Pre-trained Model**: The model must be trained and exported before using the application

## Troubleshooting

### Backend cannot load model
- Make sure you've run the `export_model.py` script from the notebook
- Verify that the `data/` folder exists and contains `.pkl` files

### Error getting games from Steam
- Verify that the profile URL is correct
- Make sure the profile is public
- Check that the backend is running on port 5000

### Frontend doesn't connect to backend
- Verify that the backend is running
- Check browser console for specific errors
- Make sure no other service is using port 5000

## Technologies Used

### Backend
- Flask - Python web framework
- Flask-CORS - CORS handling
- Pandas - Data processing
- NumPy - Numerical operations
- Scikit-learn - Machine learning model (KNN)

### Frontend
- React - UI library
- Axios - HTTP client
- CSS3 - Custom styles

## License

This project is for educational use.
