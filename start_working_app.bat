@echo off
echo Starting HealifyAI - Healthcare Assistant...
echo.

REM Activate virtual environment
echo Activating virtual environment...
call healify_env\Scripts\activate

REM Change to deployment directory
cd deployment_hf

REM Start the application
echo Starting the application...
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.
python app_minimal.py

pause 