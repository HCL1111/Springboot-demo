# Fetch SonarCloud Issues
param(
    [string]$Token = $env:SONAR_TOKEN
)

$organization = "HCL1111"
$projectKey = "HCL1111_Springboot-demo"
$baseUrl = "https://sonarcloud.io/api"

if (-not $Token) {
    Write-Host "⚠️  SONAR_TOKEN not found in environment variables" -ForegroundColor Yellow
    Write-Host "Please provide your SonarCloud token:" -ForegroundColor Cyan
    $Token = Read-Host "SonarCloud Token"
}

# Encode token for Basic Auth
$base64Token = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${Token}:"))

$headers = @{
    "Authorization" = "Basic $base64Token"
    "Accept" = "application/json"
}

Write-Host "🔍 Fetching issues from SonarCloud..." -ForegroundColor Cyan

try {
    # Fetch issues
    $issuesUrl = "$baseUrl/issues/search?componentKeys=$projectKey&ps=500"
    $response = Invoke-RestMethod -Uri $issuesUrl -Headers $headers -Method Get
    
    $issues = $response.issues
    $total = $response.total
    
    Write-Host "✅ Found $total issues" -ForegroundColor Green
    
    # Group by type
    $bugs = $issues | Where-Object { $_.type -eq "BUG" }
    $vulnerabilities = $issues | Where-Object { $_.type -eq "VULNERABILITY" }
    $codeSmells = $issues | Where-Object { $_.type -eq "CODE_SMELL" }
    $securityHotspots = $issues | Where-Object { $_.type -eq "SECURITY_HOTSPOT" }
    
    Write-Host "`n📊 Issue Summary:" -ForegroundColor Yellow
    Write-Host "  Bugs: $($bugs.Count)"
    Write-Host "  Vulnerabilities: $($vulnerabilities.Count)"
    Write-Host "  Code Smells: $($codeSmells.Count)"
    Write-Host "  Security Hotspots: $($securityHotspots.Count)"
    
    # Save to JSON file
    $outputFile = "sonarcloud-issues.json"
    $response | ConvertTo-Json -Depth 10 | Out-File $outputFile -Encoding UTF8
    Write-Host "`n💾 Issues saved to: $outputFile" -ForegroundColor Green
    
    # Create a readable summary
    $summaryFile = "sonarcloud-issues-summary.txt"
    $summary = @"
SonarCloud Issues Report
Generated: $(Get-Date)
Project: $projectKey
Organization: $organization
Total Issues: $total

=== SUMMARY BY TYPE ===
Bugs: $($bugs.Count)
Vulnerabilities: $($vulnerabilities.Count)
Code Smells: $($codeSmells.Count)
Security Hotspots: $($securityHotspots.Count)

=== DETAILED ISSUES ===

"@
    
    foreach ($issue in $issues | Sort-Object -Property severity -Descending) {
        $summary += @"
[$($issue.type)] $($issue.message)
  Severity: $($issue.severity)
  File: $($issue.component)
  Line: $($issue.line)
  Rule: $($issue.rule)
  Status: $($issue.status)
  
"@
    }
    
    $summary | Out-File $summaryFile -Encoding UTF8
    Write-Host "📄 Summary saved to: $summaryFile" -ForegroundColor Green
    
    # Return issues for further processing
    return $issues
    
} catch {
    Write-Host "❌ Error fetching SonarCloud issues: $_" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
