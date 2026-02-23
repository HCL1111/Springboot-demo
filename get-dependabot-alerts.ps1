# Fetch Dependabot Alerts from GitHub
param(
    [Parameter(Mandatory=$false)]
    [string]$Token,
    
    [Parameter(Mandatory=$false)]
    [string]$Owner = "HCL1111",
    
    [Parameter(Mandatory=$false)]
    [string]$Repo = "Springboot-demo"
)

# Check if token is provided
if (-not $Token) {
    $Token = $env:GITHUB_TOKEN
    if (-not $Token) {
        Write-Host "ERROR: GitHub token not provided!" -ForegroundColor Red
        Write-Host "Usage: .\get-dependabot-alerts.ps1 -Token 'your_github_token'" -ForegroundColor Yellow
        exit 1
    }
}

$headers = @{
    "Authorization" = "Bearer $Token"
    "Accept" = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$url = "https://api.github.com/repos/$Owner/$Repo/dependabot/alerts"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fetching Dependabot Alerts" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Repository: $Owner/$Repo" -ForegroundColor Yellow
Write-Host ""

try {
    $alerts = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
    
    if ($alerts.Count -eq 0) {
        Write-Host "No Dependabot alerts found!" -ForegroundColor Green
        exit 0
    }
    
    Write-Host "Total Alerts: $($alerts.Count)" -ForegroundColor Yellow
    Write-Host ""
    
    $counter = 1
    foreach ($alert in $alerts) {
        $severity = $alert.security_advisory.severity.ToUpper()
        $severityColor = switch ($severity) {
            "CRITICAL" { "Red" }
            "HIGH" { "Red" }
            "MODERATE" { "Yellow" }
            "LOW" { "White" }
            default { "Gray" }
        }
        
        Write-Host "[$counter] " -NoNewline -ForegroundColor Cyan
        Write-Host "$severity" -NoNewline -ForegroundColor $severityColor
        Write-Host " - $($alert.security_advisory.summary)" -ForegroundColor White
        Write-Host "    Package: $($alert.dependency.package.name) @ $($alert.dependency.manifest_path)" -ForegroundColor Gray
        Write-Host "    CVE: $($alert.security_advisory.cve_id)" -ForegroundColor Gray
        Write-Host "    GHSA: $($alert.security_advisory.ghsa_id)" -ForegroundColor Gray
        Write-Host "    State: $($alert.state)" -ForegroundColor Gray
        
        if ($alert.security_advisory.vulnerabilities.Count -gt 0) {
            $vuln = $alert.security_advisory.vulnerabilities[0]
            Write-Host "    Vulnerable Version: $($vuln.vulnerable_version_range)" -ForegroundColor Gray
            Write-Host "    Patched Version: $($vuln.first_patched_version.identifier)" -ForegroundColor Green
        }
        
        Write-Host "    Details: $($alert.html_url)" -ForegroundColor Blue
        Write-Host ""
        $counter++
    }
    
    Write-Host "========================================" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error fetching alerts: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "Note: Make sure your token has 'repo' or 'security_events' scope" -ForegroundColor Yellow
    }
}
