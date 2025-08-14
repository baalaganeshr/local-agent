Param(
	[string]$BackendPort = "8001",
	[string]$FrontendPort = "8080"
)

Write-Host "Starting backend on port $BackendPort..."
Start-Process -NoNewWindow powershell -ArgumentList "-NoExit", "-Command", "cd ..\..; uvicorn backend.api.main:app --reload --port $BackendPort"

Start-Sleep -Seconds 2
Write-Host "Starting frontend on port $FrontendPort..."
Start-Process -NoNewWindow powershell -ArgumentList "-NoExit", "-Command", "cd ..\..; npx http-server ./frontend -p $FrontendPort -c-1 --cors"
