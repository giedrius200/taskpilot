param(
    [string]$Host = '127.0.0.1',
    [int]$Port = 8000
)

Write-Host "Demo script: starting uvicorn in background..."

$env:PYTHONPATH = '.'

# Start uvicorn in a new process
$uvicorn = Start-Process -FilePath pwsh -ArgumentList "-NoLogo -NoProfile -Command \"uvicorn src.app:app --host $Host --port $Port\"" -PassThru
Start-Sleep -Seconds 1

function Invoke-Json([string]$Method, [string]$Url, $Body = $null, $Headers = $null) {
    if ($Body -ne $null) { $b = $Body | ConvertTo-Json }
    else { $b = $null }
    return Invoke-RestMethod -Method $Method -Uri $Url -ContentType 'application/json' -Body $b -Headers $Headers
}

$base = "http://$Host:$Port"
Write-Host "Using base URL: $base"

Write-Host "Registering user 'alice'..."
$r = Invoke-Json -Method Post -Url "$base/register" -Body @{ username='alice'; password='secret' }
Write-Host "Register response:"; $r

Write-Host "Logging in (JSON) to /login..."
$l = Invoke-Json -Method Post -Url "$base/login" -Body @{ username='alice'; password='secret' }
$token = $l.access_token
Write-Host "Token: $token"

Write-Host "Creating a task..."
$hdr = @{ Authorization = "Bearer $token" }
Invoke-Json -Method Post -Url "$base/tasks" -Body @{ title='Demo task from PS'; description='automated demo' } -Headers $hdr

Write-Host "Listing tasks..."
$list = Invoke-RestMethod -Method Get -Uri "$base/tasks" -Headers $hdr
$list | Format-Table

Write-Host "Stopping uvicorn process..."
Stop-Process -Id $uvicorn.Id -Force
Write-Host "Demo finished."
