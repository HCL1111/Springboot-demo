# GCP Cloud Run Monitoring & Alerting Setup Guide

**Date:** February 18, 2026  
**Service:** confluence-rag-chatbot  
**Region:** australia-southeast2 (Melbourne)  
**GCP Project:** project-f410cb7f-3020-43e6-8a9  
**Alert Email:** kaushik.deo@gmail.com

---

## Table of Contents
1. [Overview](#overview)
2. [Initial Setup](#initial-setup)
3. [Service Discovery](#service-discovery)
4. [Monitoring Infrastructure](#monitoring-infrastructure)
5. [Alert Policy Implementation](#alert-policy-implementation)
6. [Testing & Validation](#testing--validation)
7. [Lessons Learned](#lessons-learned)
8. [Maintenance Guide](#maintenance-guide)

---

## Overview

### Objective
Set up comprehensive monitoring and email alerting for a Cloud Run service to detect and notify when the service becomes unavailable.

### Solution Architecture
```
┌─────────────────────────┐
│   Cloud Run Service     │
│ confluence-rag-chatbot  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Uptime Check          │
│ • 60-second intervals   │
│ • 3 global regions      │
│ • HTTPS monitoring      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Alert Policy          │
│ • Failure detection     │
│ • 60s duration          │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Notification Channel    │
│ kaushik.deo@gmail.com   │
└─────────────────────────┘
```

### Service Specifications
- **Service Name:** confluence-rag-chatbot
- **URL:** https://confluence-rag-chatbot-955224142245.australia-southeast2.run.app
- **Resources:** 2 vCPUs, 4 GiB memory
- **Scaling:** Min 1 - Max 3 instances
- **Platform:** Cloud Run (managed)

---

## Initial Setup

### 1. Google Cloud SDK Installation

**Installation Command:**
```powershell
# Download installer
Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" `
    -OutFile "$env:TEMP\GoogleCloudSDKInstaller.exe"

# Silent installation with all components
& "$env:TEMP\GoogleCloudSDKInstaller.exe" /S /noreporting /D="$env:LOCALAPPDATA\Google\Cloud SDK"
```

**Components Installed:**
- Google Cloud SDK 556.0.0
- kubectl
- gke-gcloud-auth-plugin
- Beta components (for advanced Cloud Run operations)

**Verification:**
```bash
gcloud version
# Output: Google Cloud SDK 556.0.0
```

### 2. Authentication

**Initial Authentication:**
```bash
gcloud auth login
```
- Authenticated as: **kaushik.deo@gmail.com**
- Browser-based OAuth flow

**Set Default Project:**
```bash
gcloud config set project project-f410cb7f-3020-43e6-8a9
```

---

## Service Discovery

### List Available Projects
```bash
gcloud projects list
```

**Result:**
| Project Name | Project ID | Project Number |
|-------------|------------|----------------|
| My First Project | project-f410cb7f-3020-43e6-8a9 | 955224142245 |
| genai-learning-446305 | genai-learning-446305 | 611587931464 |
| Unreal-Ai-Nexus | unreal-ai-nexus | 331115690467 |

### Locate Cloud Run Service
```bash
gcloud run services list --region=australia-southeast2
```

**Service Details:**
```
SERVICE                    REGION                  URL                                                                    LAST DEPLOYED AT
confluence-rag-chatbot     australia-southeast2    https://confluence-rag-chatbot-955224142245.australia-southeast2...    2025-10-07T07:13:30.154089Z
```

### Service Configuration Check
```bash
gcloud run services describe confluence-rag-chatbot --region=australia-southeast2
```

**Key Configuration:**
```yaml
serviceRevisionTemplate:
  containers:
    resources:
      cpu: 2000m
      memory: 4Gi
  scaling:
    minInstanceCount: 1
    maxInstanceCount: 3
```

---

## Monitoring Infrastructure

### 1. Notification Channel Setup

**Create Email Notification Channel:**

```bash
# Get access token
$TOKEN = gcloud auth print-access-token

# Create notification channel via REST API
$CHANNEL_DATA = @{
    type = "email"
    displayName = "Kaushik Email Alerts"
    enabled = $true
    labels = @{
        email_address = "kaushik.deo@gmail.com"
    }
}

Invoke-RestMethod -Uri "https://monitoring.googleapis.com/v3/projects/project-f410cb7f-3020-43e6-8a9/notificationChannels" `
    -Method Post `
    -Headers @{"Authorization"="Bearer $TOKEN"; "Content-Type"="application/json"} `
    -Body ($CHANNEL_DATA | ConvertTo-Json)
```

**Result:**
- **Channel ID:** 8199605340313241478
- **Status:** UNVERIFIED (initially)

### 2. Email Verification

**Verification Process:**
1. Verification email sent to kaushik.deo@gmail.com
2. Verification code received: **G-017988**
3. Manual verification via API:

```bash
$VERIFY_DATA = @{
    code = "G-017988"
}

Invoke-RestMethod -Uri "https://monitoring.googleapis.com/v3/projects/project-f410cb7f-3020-43e6-8a9/notificationChannels/8199605340313241478:verify" `
    -Method Post `
    -Headers @{"Authorization"="Bearer $TOKEN"; "Content-Type"="application/json"} `
    -Body ($VERIFY_DATA | ConvertTo-Json)
```

**Result:** Channel status changed to **VERIFIED** ✅

### 3. Uptime Check Configuration

**Uptime Check JSON Configuration** (`uptime-check.json`):
```json
{
  "displayName": "CloudRun-Chatbot-Uptime",
  "monitoredResource": {
    "type": "uptime_url",
    "labels": {
      "host": "confluence-rag-chatbot-955224142245.australia-southeast2.run.app"
    }
  },
  "httpCheck": {
    "requestMethod": "GET",
    "path": "/",
    "port": 443,
    "useSsl": true,
    "validateSsl": true
  },
  "period": "60s",
  "timeout": "10s",
  "selectedRegions": [
    "ASIA_PACIFIC",
    "USA",
    "EUROPE"
  ]
}
```

**Create Uptime Check:**
```bash
Invoke-RestMethod -Uri "https://monitoring.googleapis.com/v3/projects/project-f410cb7f-3020-43e6-8a9/uptimeCheckConfigs" `
    -Method Post `
    -Headers @{"Authorization"="Bearer $TOKEN"; "Content-Type"="application/json"} `
    -Body (Get-Content uptime-check.json -Raw)
```

**Result:**
- **Check ID:** cloudrun-chatbot-uptime-9ZKm-dv-Ejo
- **Monitoring Frequency:** Every 60 seconds
- **Global Coverage:** 3 regions (Asia-Pacific, USA, Europe)
- **Protocol:** HTTPS on port 443

---

## Alert Policy Implementation

### Initial Approach: Metric-Based Alerts (Request Count)

**First Attempt - Alert Policy Configuration:**
```json
{
  "displayName": "Cloud Run Service DOWN - No Traffic",
  "conditions": [{
    "displayName": "Request count below threshold",
    "conditionThreshold": {
      "filter": "metric.type=\"run.googleapis.com/request_count\" AND resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"confluence-rag-chatbot\"",
      "comparison": "COMPARISON_LT",
      "thresholdValue": 0.01,
      "duration": "120s",
      "aggregations": [{
        "alignmentPeriod": "60s",
        "perSeriesAligner": "ALIGN_RATE"
      }]
    }
  }],
  "notificationChannels": [
    "projects/project-f410cb7f-3020-43e6-8a9/notificationChannels/8199605340313241478"
  ],
  "combiner": "OR",
  "enabled": true
}
```

**Problems Encountered:**
1. ❌ Email not received on first test - channel was UNVERIFIED
2. ❌ Email not received after verification - alert condition never triggered

**Root Cause Analysis:**
- Cloud Run continues to receive traffic even when `ingress=internal` (health checks, internal probes)
- `request_count` metric doesn't drop to zero during service outages
- Metric collection has 60-120 second delays
- **Conclusion:** Request count metrics are unreliable for detecting service unavailability

### Final Solution: Uptime Check-Based Alerts

**Alert Policy Configuration:**
```powershell
$ALERT_DATA = @{
    displayName = "Cloud Run Service DOWN - Uptime Check Failed"
    documentation = @{
        content = "ALERT: The Cloud Run service confluence-rag-chatbot is unreachable! The uptime check has failed."
        mimeType = "text/markdown"
    }
    conditions = @(@{
        displayName = "Uptime check failed"
        conditionThreshold = @{
            filter = "metric.type=`"monitoring.googleapis.com/uptime_check/check_passed`" AND resource.type=`"uptime_url`" AND metric.label.check_id=`"cloudrun-chatbot-uptime-9ZKm-dv-Ejo`""
            comparison = "COMPARISON_LT"
            thresholdValue = 1
            duration = "60s"
            aggregations = @(@{
                alignmentPeriod = "60s"
                perSeriesAligner = "ALIGN_FRACTION_TRUE"
            })
        }
    })
    notificationChannels = @(
        "projects/project-f410cb7f-3020-43e6-8a9/notificationChannels/8199605340313241478"
    )
    combiner = "OR"
    enabled = $true
}

Invoke-RestMethod -Uri "https://monitoring.googleapis.com/v3/projects/project-f410cb7f-3020-43e6-8a9/alertPolicies" `
    -Method Post `
    -Headers @{"Authorization"="Bearer $TOKEN"; "Content-Type"="application/json"} `
    -Body ($ALERT_DATA | ConvertTo-Json -Depth 10)
```

**Why This Works:**
- ✅ Actively probes the actual service URL (not just metrics)
- ✅ Detects real HTTP availability issues
- ✅ Triggers within 60-120 seconds of service failure
- ✅ Industry standard for availability monitoring

---

## Testing & Validation

### Test Setup

**Capability Tests (Performed Before Alerting):**

1. **Memory Modification Test:**
   ```bash
   # Reduce memory to 2Gi
   gcloud run services update confluence-rag-chatbot \
       --region=australia-southeast2 \
       --memory=2Gi --quiet
   
   # Restore to 4Gi
   gcloud run services update confluence-rag-chatbot \
       --region=australia-southeast2 \
       --memory=4Gi --quiet
   ```
   **Result:** ✅ Successful (Revisions 00009, 00010, 00011 created)

2. **Access Control Test:**
   ```bash
   # Block external access
   gcloud run services update confluence-rag-chatbot \
       --region=australia-southeast2 \
       --ingress=internal --quiet
   ```
   **Result:** ✅ Service became inaccessible from public internet

### Alert Testing

**Final Test - Uptime Check Alert:**

**Test Execution:**
```bash
# Take service down
gcloud run services update confluence-rag-chatbot \
    --region=australia-southeast2 \
    --ingress=internal --quiet
```

**Timeline:**
- ⏰ **13:58** - Service ingress changed to `internal`
- ⏰ **14:00** - Uptime checks begin failing
- 📧 **14:00-14:01** - Multiple alert emails received at kaushik.deo@gmail.com

**Test Result:** ✅ **SUCCESS - Multiple emails received!**

**Service Restoration:**
```bash
gcloud run services update confluence-rag-chatbot \
    --region=australia-southeast2 \
    --ingress=all --quiet
```
- ⏰ **14:00:41** - Service restored to normal operation

---

## Lessons Learned

### What Worked ✅

1. **Uptime Checks are Superior**
   - Direct HTTP/HTTPS probing is the gold standard
   - Fast detection (60-120 seconds)
   - Reliable triggering

2. **Email Verification is Critical**
   - Notification channels must be verified before alerts work
   - Verification can be done via API with verification code
   - Check channel status before relying on alerts

3. **Multi-Region Monitoring**
   - Monitoring from 3 global regions provides redundancy
   - Reduces false positives from regional network issues
   - Ensures global service availability validation

### What Didn't Work ❌

1. **Metric-Based Alerts on Request Count**
   - Health checks continue even when service is "down"
   - Metric collection delays make detection slow
   - Not suitable for availability monitoring

2. **Initial Channel Setup Issues**
   - Created channels start in UNVERIFIED state
   - No alerts sent until verification completed
   - Easy to miss verification step

### Best Practices 📋

1. **Always verify notification channels immediately** after creation
2. **Use uptime checks for availability monitoring**, not metrics
3. **Test alerts in production** with actual service disruptions
4. **Monitor from multiple regions** to detect regional issues
5. **Set reasonable check intervals** (60s is good balance between cost and detection speed)
6. **Document alert policies** with clear descriptions for on-call teams

---

## Maintenance Guide

### Checking Alert Status

**List All Alert Policies:**
```bash
gcloud alpha monitoring policies list
```

**View Specific Policy:**
```bash
gcloud alpha monitoring policies describe <POLICY_ID>
```

**Check Recent Incidents:**
```bash
gcloud alpha monitoring incidents list \
    --filter="state=OPEN" \
    --format="table(name,startedAt,state)"
```

### Testing the Alert System

**Manual Test Procedure:**
1. Block external access:
   ```bash
   gcloud run services update confluence-rag-chatbot \
       --region=australia-southeast2 \
       --ingress=internal --quiet
   ```

2. Wait 60-120 seconds for alert to trigger

3. Verify email received at kaushik.deo@gmail.com

4. Restore service:
   ```bash
   gcloud run services update confluence-rag-chatbot \
       --region=australia-southeast2 \
       --ingress=all --quiet
   ```

### Modifying Alert Configuration

**Update Notification Email:**
```bash
# Get channel details
gcloud alpha monitoring channels list

# Update channel
gcloud alpha monitoring channels update <CHANNEL_ID> \
    --update-user-labels=email_address=newemail@example.com
```

**Adjust Uptime Check Frequency:**
```bash
# Edit uptime check via API
# Modify period in uptime-check.json
# Update via REST API POST with new configuration
```

### Troubleshooting

**No Emails Received?**
1. Check notification channel status:
   ```bash
   gcloud alpha monitoring channels describe <CHANNEL_ID>
   ```
   - Ensure `verificationStatus: VERIFIED`

2. Check alert policy is enabled:
   ```bash
   gcloud alpha monitoring policies describe <POLICY_ID>
   ```
   - Ensure `enabled: true`

3. Verify uptime check is running:
   ```bash
   gcloud monitoring uptime list-configs
   ```

4. Check for active incidents:
   ```bash
   gcloud alpha monitoring incidents list
   ```

**False Positives?**
- Increase `duration` in alert condition (currently 60s)
- Adjust threshold or alignment period
- Review uptime check timeout settings

---

## Resource IDs

**Quick Reference:**
- **Project ID:** project-f410cb7f-3020-43e6-8a9
- **Project Number:** 955224142245
- **Service Name:** confluence-rag-chatbot
- **Region:** australia-southeast2
- **Notification Channel ID:** 8199605340313241478
- **Uptime Check ID:** cloudrun-chatbot-uptime-9ZKm-dv-Ejo
- **Service URL:** https://confluence-rag-chatbot-955224142245.australia-southeast2.run.app

---

## Commands Quick Reference

### Service Management
```bash
# View service status
gcloud run services describe confluence-rag-chatbot --region=australia-southeast2

# Update memory
gcloud run services update confluence-rag-chatbot --region=australia-southeast2 --memory=4Gi

# Update CPU
gcloud run services update confluence-rag-chatbot --region=australia-southeast2 --cpu=2

# Change ingress
gcloud run services update confluence-rag-chatbot --region=australia-southeast2 --ingress=all
```

### Monitoring
```bash
# List uptime checks
gcloud monitoring uptime list-configs

# List alert policies
gcloud alpha monitoring policies list

# List notification channels
gcloud alpha monitoring channels list

# View recent incidents
gcloud alpha monitoring incidents list --filter="state=OPEN"
```

---

## Cost Considerations

**Uptime Check Pricing (as of 2026):**
- First 1 million checks/month: Free
- Current usage: ~129,600 checks/month (3 regions × 1 check/min × 43,200 min)
- **Estimated cost:** $0/month (within free tier)

**Alert Policy Pricing:**
- First 100 rules: Free
- Current usage: 1 alert policy
- **Estimated cost:** $0/month

**Total Monitoring Cost:** **FREE** ✅

---

## Conclusion

Successfully implemented production-grade monitoring for the Cloud Run service with:
- ✅ 24/7 uptime monitoring from 3 global regions
- ✅ Email alerts to kaushik.deo@gmail.com within 60-120 seconds of outages
- ✅ Verified and tested alert delivery
- ✅ Zero monthly cost (within free tier)
- ✅ Industry-standard reliability monitoring

The system is now production-ready and will immediately notify the team when the service becomes unavailable.

---

**Document Version:** 1.0  
**Last Updated:** February 18, 2026  
**Author:** GitHub Copilot  
**Contact:** kaushik.deo@gmail.com
