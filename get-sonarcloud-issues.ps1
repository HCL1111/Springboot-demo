# Get detailed SonarCloud issues
param(
    [Parameter(Mandatory=$false)]
    [string]$Token = "f35fc999f013f488d5332430b4c55150f86343f0",
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectKey = "HCL1111_Springboot-demo"
)

$base64Token = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${Token}:"))
$headers = @{
    "Authorization" = "Basic $base64Token"
    "Accept" = "application/json"
}

$baseUrl = "https://sonarcloud.io/api"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SonarCloud Issues Details" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get all open issues
$issuesUrl = "$baseUrl/issues/search?componentKeys=$ProjectKey&resolved=false&ps=100"
$response = Invoke-RestMethod -Uri $issuesUrl -Headers $headers -Method Get

Write-Host "Total Issues: $($response.total)" -ForegroundColor Yellow
Write-Host ""

$counter = 1
foreach ($issue in $response.issues) {
    $severityColor = switch ($issue.severity) {
        "BLOCKER" { "Red" }
        "CRITICAL" { "Red" }
        "MAJOR" { "Yellow" }
        "MINOR" { "White" }
        "INFO" { "Gray" }
        default { "White" }
    }
    
    Write-Host "[$counter] " -NoNewline -ForegroundColor Cyan
    Write-Host "$($issue.severity)" -NoNewline -ForegroundColor $severityColor
    Write-Host " - $($issue.type)" -ForegroundColor White
    
    Write-Host "    Rule: $($issue.rule)" -ForegroundColor Gray
    Write-Host "    Message: $($issue.message)" -ForegroundColor White
    Write-Host "    File: $($issue.component.Split(':')[-1])" -ForegroundColor Gray
    
    if ($issue.line) {
        Write-Host "    Line: $($issue.line)" -ForegroundColor Gray
    }
    
    Write-Host "    Status: $($issue.status) | Effort: $($issue.effort)" -ForegroundColor Gray
    Write-Host ""
    $counter++
}

Write-Host "========================================" -ForegroundColor Cyan
