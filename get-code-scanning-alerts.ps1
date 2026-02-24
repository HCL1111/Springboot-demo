# Get Code Scanning Alerts from GitHub
$repo = "HCL1111/Springboot-demo"
$apiUrl = "https://api.github.com/repos/$repo/code-scanning/alerts"

try {
    Write-Host "Fetching code scanning alerts from $repo..." -ForegroundColor Cyan
    
    # Fetch alerts
    $response = Invoke-RestMethod -Uri $apiUrl -Headers @{
        "Accept" = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
    } -ErrorAction Stop
    
    # Count by rule type
    $totalAlerts = $response.Count
    $codeSmells = ($response | Where-Object { $_.rule.tags -contains "maintainability" -or $_.rule.severity -eq "note" -or $_.rule.severity -eq "warning" }).Count
    $bugs = ($response | Where-Object { $_.rule.tags -contains "correctness" }).Count
    $vulnerabilities = ($response | Where-Object { $_.rule.tags -contains "security" }).Count
    
    Write-Host "`nCode Scanning Summary:" -ForegroundColor Green
    Write-Host "=====================" -ForegroundColor Green
    Write-Host "Total Alerts: $totalAlerts"
    Write-Host "Code Smells (maintainability/warnings): $codeSmells"
    Write-Host "Bugs: $bugs"
    Write-Host "Vulnerabilities: $vulnerabilities"
    
    Write-Host "`nDetailed breakdown:" -ForegroundColor Yellow
    $response | Group-Object -Property { $_.rule.severity } | ForEach-Object {
        Write-Host "  $($_.Name): $($_.Count)"
    }
    
    # Show top issues
    Write-Host "`nTop 10 issues:" -ForegroundColor Cyan
    $response | Select-Object -First 10 | ForEach-Object {
        Write-Host "  - [$($_.rule.severity)] $($_.rule.description)" -ForegroundColor Gray
        Write-Host "    File: $($_.most_recent_instance.location.path):$($_.most_recent_instance.location.start_line)" -ForegroundColor DarkGray
    }
    
} catch {
    Write-Host "Error fetching code scanning alerts: $_" -ForegroundColor Red
    Write-Host "You may need to authenticate with GitHub CLI: gh auth login" -ForegroundColor Yellow
}
