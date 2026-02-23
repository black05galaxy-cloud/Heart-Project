# Heart Collaborative — Heart Risk AI

AI-based heart attack risk prediction using retinal fundus images. Medical theme UI with Dashboard, New Analysis, Results & History, and Settings.

## 🌐 Application link — open for everyone

**Want everyone to access your app from any device?**

👉 **Deploy it for free** → Get a public link like `https://heart-project-xxxx.streamlit.app`  
👉 **See the "Deploy" page** in the app navigation (or read **[DEPLOY_SIMPLE.md](DEPLOY_SIMPLE.md)**)

**Quick options:**
- **Local (your computer only):** Run `streamlit run app.py` → Open **http://localhost:8501**
- **Public (everyone, any device):** Deploy to Streamlit Cloud → Get **https://your-app-name.streamlit.app** (free, 5 minutes)

## How to run locally (no sign-in required)

You do **not** need to sign in to Streamlit or any service to run the app on your computer.

### Option A — Double-click to open (Windows)

1. Double-click **`run_app.bat`** in this folder.
2. Wait a few seconds. Your browser should open to the app.
3. If the browser does not open, open it yourself and go to: **http://localhost:8501**

### Option B — Run from terminal (install packages, then run)

1. Open a **terminal** (Command Prompt, PowerShell, or VS Code terminal) in this project folder.
2. **Install required packages** (run once):
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the app**:
   ```bash
   streamlit run app.py
   ```
4. Open your browser and go to: **http://localhost:8501** (or let it open automatically).

**One-line (install + run):**
   ```bash
   pip install -r requirements.txt && streamlit run app.py
   ```

**PowerShell (Windows):** From this folder, run:
   ```powershell
   .\run.ps1
   ```
   This installs packages and starts the app; the browser will open at **http://localhost:8501**.

### App won’t open or sign-in issues?

- **No sign-in needed** when running locally. Ignore any Streamlit Cloud or “sign in” prompts.
- If the browser never opens, type this in your browser address bar: **http://localhost:8501**
- If you see “Cannot connect”, wait 10–15 seconds after starting the app and try again.
- Make sure nothing else is using port 8501 (e.g. another Streamlit app).

## Features

- **Dashboard** — White font on dark medical theme; KPIs, risk distribution, trend chart, recent activity.
- **New Analysis** — Patient info, clinical parameters, retinal image upload, RUN V5.2 ANALYSIS, gauge and recommendations.
- **Results & History** — Filter, export CSV, view past analyses and recommendations.
- **Settings** — Model version, clear history, about.

*Heart Collaborative · Medical AI · Demo only — not a substitute for professional medical advice.*
