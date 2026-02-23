@echo off
title Heart Collaborative - Heart Risk AI
cd /d "%~dp0"

echo.
echo  Heart Collaborative - Starting app (no sign-in required)
echo  ----------------------------------------
echo.

REM Ensure dependencies are installed
echo Checking dependencies...
pip install -r requirements.txt -q

echo Opening app in your browser in a few seconds...
echo If the browser does not open, go to:  http://localhost:8501
echo.

REM Open browser after 5 seconds (gives Streamlit time to start)
start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8501"

REM Run Streamlit (this keeps the window open)
streamlit run app.py

pause
