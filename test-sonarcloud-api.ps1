# SonarCloud API Testing Script
# This script fetches project data from SonarCloud API

param(
    [Parameter(Mandatory=$false)]
    [string]$Token,
    
    [Parameter(Mandatory=$false)]
    [string]$Organization = "HCL1111",
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectKey = "HCL1111_Springboot-demo"
)

# Check if token is provided or in environment
if (-not $Token) {
    $Token = $env:SONAR_TOKEN
    if (-not $Token) {
        Write-Host "ERROR: SonarCloud token not provided!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please provide token in one of these ways:" -ForegroundColor Yellow
        Write-Host "1. As parameter: .\test-sonarcloud-api.ps1 -Token 'your_token_here'"
        Write-Host "2. As environment variable: `$env:SONAR_TOKEN = 'your_token_here'"
        Write-Host ""
        Write-Host "Get your token from: https://sonarcloud.io/account/security" -ForegroundColor Cyan
        exit 1
    }
}

# Base64 encode the token for basic auth (token as username, empty password)
$base64Token = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${Token}:"))
$headers = @{
    "Authorization" = "Basic $base64Token"
    "Accept" = "application/json"
}

$baseUrl = "https://sonarcloud.io/api"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SonarCloud API Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Organization: $Organization" -ForegroundColor Yellow
Write-Host "Project Key: $ProjectKey" -ForegroundColor Yellow
Write-Host ""

# Test 1: Get Project Information
Write-Host "[1/4] Fetching Project Information..." -ForegroundColor Green
try {
    $projectUrl = "$baseUrl/project_analyses/search?project=$ProjectKey"
    $projectResponse = Invoke-RestMethod -Uri $projectUrl -Headers $headers -Method Get
    
    if ($projectResponse.analyses.Count -gt 0) {
        $latestAnalysis = $projectResponse.analyses[0]
        Write-Host "  ✓ Project found!" -ForegroundColor Green
        Write-Host "  Latest Analysis Date: $($latestAnalysis.date)" -ForegroundColor White
        Write-Host ""
    }
} catch {
    Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 2: Get Quality Gate Status
Write-Host "[2/4] Fetching Quality Gate Status..." -ForegroundColor Green
try {
    $qgUrl = "$baseUrl/qualitygates/project_status?projectKey=$ProjectKey"
    $qgResponse = Invoke-RestMethod -Uri $qgUrl -Headers $headers -Method Get
    
    $status = $qgResponse.projectStatus.status
    $statusColor = if ($status -eq "OK") { "Green" } elseif ($status -eq "ERROR") { "Red" } else { "Yellow" }
    
    Write-Host "  ✓ Quality Gate Status: $status" -ForegroundColor $statusColor
    
    if ($qgResponse.projectStatus.conditions) {
        Write-Host "  Conditions:" -ForegroundColor White
        foreach ($condition in $qgResponse.projectStatus.conditions) {
            $condStatus = if ($condition.status -eq "OK") { "✓" } else { "✗" }
            Write-Host "    $condStatus $($condition.metricKey): $($condition.actualValue) (threshold: $($condition.errorThreshold))" -ForegroundColor White
        }
    }
    Write-Host ""
} catch {
    Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 3: Get Issues Summary
Write-Host "[3/4] Fetching Issues Summary..." -ForegroundColor Green
try {
    $issuesUrl = "$baseUrl/issues/search?componentKeys=$ProjectKey&ps=1&facets=severities,types"
    $issuesResponse = Invoke-RestMethod -Uri $issuesUrl -Headers $headers -Method Get
    
    Write-Host "  ✓ Total Issues Found: $($issuesResponse.total)" -ForegroundColor White
    
    if ($issuesResponse.facets) {
        foreach ($facet in $issuesResponse.facets) {
            if ($facet.property -eq "severities") {
                Write-Host "  By Severity:" -ForegroundColor White
                foreach ($value in $facet.values) {
                    Write-Host "    - $($value.val): $($value.count)" -ForegroundColor White
                }
            }
            if ($facet.property -eq "types") {
                Write-Host "  By Type:" -ForegroundColor White
                foreach ($value in $facet.values) {
                    Write-Host "    - $($value.val): $($value.count)" -ForegroundColor White
                }
            }
        }
    }
    Write-Host ""
} catch {
    Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 4: Get Measures (Code Metrics)
Write-Host "[4/4] Fetching Code Metrics..." -ForegroundColor Green
try {
    $metricsUrl = "$baseUrl/measures/component?component=$ProjectKey&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,ncloc,security_hotspots"
    $metricsResponse = Invoke-RestMethod -Uri $metricsUrl -Headers $headers -Method Get
    
    Write-Host "  ✓ Metrics Retrieved:" -ForegroundColor White
    foreach ($measure in $metricsResponse.component.measures) {
        $metricName = $measure.metric
        $value = if ($measure.value) { $measure.value } else { "N/A" }
        Write-Host "    - ${metricName}: $value" -ForegroundColor White
    }
    Write-Host ""
} catch {
    Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "API Test Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
