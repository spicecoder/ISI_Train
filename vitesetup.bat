@echo off
:: Set the project name
set /p project_name="Enter your project name: "

:: Check if a project name was entered
if "%project_name%"=="" (
    echo You must provide a project name.
    exit /b
)

:: Create the Vite project
echo Creating Vite project "%project_name%"...
npx create-vite@latest %project_name% --template react

:: Navigate to the project directory
cd %project_name%

:: Install dependencies
echo Installing dependencies...
npm install

:: Start the development server
echo Starting the development server...
npm run dev
pause
