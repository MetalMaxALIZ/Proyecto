# 🚀 Quick Start - What Should I Play?

## Steps to run the application

### 1️⃣ Export the Model (First time only)

1. Open `pruebas.ipynb` notebook in VS Code
2. Run all cells sequentially
3. At the end of the notebook, run the cell titled "**Export Model for Frontend**"
4. You'll see a confirmation message indicating data was saved in the `data/` folder

### 2️⃣ Start Backend

Option A - Using automatic script:
```powershell
.\start_backend.bat
```

Option B - Manual:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Backend will be running at: **http://localhost:5000**

### 3️⃣ Start Frontend

**Open a new terminal** and run:

Option A - Using automatic script:
```powershell
.\start_frontend.bat
```

Option B - Manual:
```powershell
cd frontend
npm install
npm start
```

Frontend will automatically open at: **http://localhost:3000**

## ✅ Ready to use!

1. Enter your Steam profile URL (must be public)
2. Click "Get Games"
3. Select the games you like
4. Click "WSIP" to get recommendations

## ⚠️ Troubleshooting

### "data folder not found"
- Run the export cell in `pruebas.ipynb` notebook

### "Error connecting to server"
- Make sure backend is running on port 5000
- Verify no firewall is blocking the connection

### "Could not get games"
- Verify your Steam profile is public
- Check that the profile URL is correct

## 📝 Notes

- First time will take longer because it needs to install dependencies
- You need Python 3.8+ and Node.js 14+ installed
- Steam profile MUST be public to retrieve games

## 🎮 Enjoy discovering new games!
