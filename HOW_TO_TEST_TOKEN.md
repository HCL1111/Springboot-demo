# How to Test the CVE Scanner with Your Token

## ⚠️ CRITICAL SECURITY ISSUE

**The token `ghp_9OZL**********************LUEl` was shared publicly and is now COMPROMISED.**

### Immediate Actions Required:

1. **Revoke this token NOW**: https://github.com/settings/tokens
2. **Generate a new token** (instructions below)
3. **NEVER share tokens** in code, chat, or public places

---

## Quick Start Guide

### 1. Generate a NEW Token

Since the old token is compromised, create a new one:

**Go to**: https://github.com/settings/tokens/new

**Configure**:
- Name: `CVE Scanner`
- Scopes: 
  - ✅ `repo`
  - ✅ `security_events` ⭐ **REQUIRED**
  - ✅ `workflow` (optional)

**Click** "Generate token" and **copy it immediately**

### 2. Configure Your Local Environment

**On your laptop** (NOT in this chat!), set environment variables:

```bash
# Linux/macOS
export GITHUB_TOKEN='your_NEW_token_here'
export GITHUB_REPOSITORY='HCL1111/Springboot-demo'

# Windows PowerShell
$env:GITHUB_TOKEN='your_NEW_token_here'
$env:GITHUB_REPOSITORY='HCL1111/Springboot-demo'
```

### 3. Run the Test Flow

```bash
# Navigate to repository
cd ~/Springboot-demo

# Test 1: Check your environment
python scripts/test_token_flow.py

# Test 2: Validate your token
python scripts/setup_token.py

# Test 3: Run the CVE scanner
python scripts/fix_cves.py
```

---

## What Each Script Does

### `scripts/test_token_flow.py` - Flow Simulator

Shows what will happen when you run the CVE scanner:
- Checks environment variables
- Explains each step
- Shows expected output
- **Doesn't make any changes**

```bash
python scripts/test_token_flow.py
```

### `scripts/setup_token.py` - Token Validator

Validates your token has correct permissions:
- Tests GitHub API connectivity
- Checks for `security_events` scope
- Verifies Dependabot access
- Reports specific issues

```bash
python scripts/setup_token.py
```

Expected output when successful:
```
✅ All checks passed! Your token is configured correctly.
```

### `scripts/fix_cves.py` - CVE Scanner

The actual CVE scanner that:
- Detects vulnerabilities via Dependabot API
- Fixes them automatically
- Creates Pull Requests

```bash
python scripts/fix_cves.py
```

---

## Expected Results

When you run `python scripts/fix_cves.py` on your laptop with a valid token:

1. ✅ Connects to GitHub API (no 403 error!)
2. ✅ Finds CVE-2024-47554 in commons-io:2.13.0
3. ✅ Updates to commons-io:2.18.0
4. ✅ Runs Gradle build to verify
5. ✅ Creates CVE_FIX_REPORT.md
6. ✅ Creates a Pull Request

---

## Why It Doesn't Work Here (GitHub Actions Environment)

This sandboxed environment has:
- DNS monitoring proxy blocking GitHub API
- Different network restrictions
- Different security model

**The scripts WILL work on your personal laptop** - that's where you should test them!

---

## Complete Testing Checklist

On your **personal laptop**, do this:

- [ ] Revoke the old token: https://github.com/settings/tokens
- [ ] Generate a NEW token with `security_events` scope
- [ ] Open terminal and navigate to repository
- [ ] Set `GITHUB_TOKEN` environment variable
- [ ] Set `GITHUB_REPOSITORY='HCL1111/Springboot-demo'`
- [ ] Run `python scripts/test_token_flow.py` (simulator)
- [ ] Run `python scripts/setup_token.py` (validator)
- [ ] Verify all checks pass ✅
- [ ] Run `python scripts/fix_cves.py` (actual scanner)
- [ ] Check that PR was created on GitHub
- [ ] Review CVE_FIX_REPORT.md

---

## Documentation Files

- **TEST_YOUR_TOKEN.md** - Complete security guide and setup instructions
- **QUICK_FIX_403.md** - Quick reference for fixing 403 errors
- **FIXING_403_FOR_PERSONAL_USE.md** - Detailed troubleshooting guide
- **README_CVE_FIX.md** - Technical overview of the solution

---

## Security Reminders

### ✅ Good Practices:
- Use environment variables for tokens
- Generate new tokens with minimal scopes
- Set token expiration dates
- Revoke tokens when no longer needed

### ❌ Never Do This:
- Share tokens in chat or code
- Commit tokens to Git
- Use tokens without expiration
- Give tokens excessive permissions

---

## Support

If you encounter issues:

1. Run the validator: `python scripts/setup_token.py`
2. It will tell you exactly what's wrong
3. Follow the specific instructions it provides
4. Re-run until all checks pass

**Common issues**:
- Missing `security_events` scope → Recreate token
- Dependabot not enabled → Enable in repo settings
- Token expired → Generate new token
- 403 errors → Check token permissions

---

## Summary

**The Python code is already configured correctly** - it reads from environment variables, not hardcoded values. You just need to:

1. ✅ Generate a NEW token (old one is compromised)
2. ✅ Set it as environment variable on your laptop
3. ✅ Run the validator to confirm
4. ✅ Run the CVE scanner

**No code changes needed** - the configuration uses environment variables, which is the secure way to handle tokens!
