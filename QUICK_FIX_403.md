# Quick Fix for 403 Errors on Personal Laptop

## TL;DR - 3 Steps to Fix

### Step 1: Run the Validator
```bash
python scripts/setup_token.py
```

### Step 2: Create Token with Correct Permissions

Go to: **https://github.com/settings/tokens/new**

Select these scopes:
- ✅ `repo` (Full control of private repositories)
- ✅ `security_events` ⭐ **THIS IS THE KEY!**

### Step 3: Set Environment Variables

**Linux/Mac:**
```bash
export GITHUB_TOKEN='your_token_here'
export GITHUB_REPOSITORY='HCL1111/Springboot-demo'
```

**Windows PowerShell:**
```powershell
$env:GITHUB_TOKEN='your_token_here'
$env:GITHUB_REPOSITORY='HCL1111/Springboot-demo'
```

**Windows CMD:**
```cmd
set GITHUB_TOKEN=your_token_here
set GITHUB_REPOSITORY=HCL1111/Springboot-demo
```

## Why This Fixes It

The 403 error happens because:

❌ **You have a token with only `repo` scope**  
✅ **You need `security_events` scope for Dependabot API**

## Verify It Works

```bash
# Run validator - should now pass all checks
python scripts/setup_token.py

# Expected output:
# ✅ All checks passed! Your token is configured correctly.
```

## Run the CVE Scanner

```bash
python scripts/fix_cves.py
```

Should now work without 403 errors!

## Full Documentation

For complete details, see:
- **[FIXING_403_FOR_PERSONAL_USE.md](FIXING_403_FOR_PERSONAL_USE.md)** - Full setup guide
- **[README_CVE_FIX.md](README_CVE_FIX.md)** - Complete solution overview

## Still Having Issues?

The validator will tell you exactly what's wrong:

```bash
python scripts/setup_token.py
```

Common issues it detects:
- ❌ Token missing `security_events` scope
- ❌ Dependabot not enabled
- ❌ Token expired
- ❌ Wrong repository access

It provides specific fix instructions for each issue!
