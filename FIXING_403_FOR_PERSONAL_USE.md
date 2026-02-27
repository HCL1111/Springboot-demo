# Fixing 403 Errors for Personal GitHub Accounts

## The Real Issue

When running the CVE scanner on your **personal laptop** with a **personal GitHub account**, you get 403 Forbidden errors. This is **NOT** the same as the DNS proxy issue - this is a **token permissions problem**.

## Root Cause

The GitHub Dependabot API requires specific permissions that are different from regular API access:

1. **Regular repo access** ≠ **Security events access**
2. Personal Access Tokens need the **`security_events`** scope
3. Dependabot must be **enabled** in repository settings
4. The token must have access to the **specific repository**

## Complete Fix (Step-by-Step)

### Step 1: Create a GitHub Personal Access Token

#### For Classic Tokens (Easier):

1. Go to: **https://github.com/settings/tokens**

2. Click **"Generate new token"** → **"Generate new token (classic)"**

3. Fill in the form:
   - **Note**: `CVE Scanner for Springboot-demo`
   - **Expiration**: Choose your preference (90 days recommended)
   
4. **Select these scopes** (IMPORTANT):
   ```
   ✓ repo
     ✓ repo:status
     ✓ repo_deployment
     ✓ public_repo
     ✓ repo:invite
     ✓ security_events  ← THIS IS CRITICAL!
   
   ✓ workflow (if you plan to trigger workflows)
   ```

5. Click **"Generate token"**

6. **COPY THE TOKEN** - You won't see it again!

#### For Fine-grained Tokens (More Secure):

1. Go to: **https://github.com/settings/tokens?type=beta**

2. Click **"Generate new token"**

3. Fill in:
   - **Token name**: `CVE Scanner`
   - **Expiration**: 90 days (or your preference)
   - **Repository access**: 
     - Select **"Only select repositories"**
     - Choose **`HCL1111/Springboot-demo`** (or your repository)

4. **Set Permissions**:
   ```
   Repository permissions:
   ✓ Contents: Read and write
   ✓ Metadata: Read-only (auto-selected)
   ✓ Pull requests: Read and write
   ✓ Security events: Read-only  ← THIS IS CRITICAL!
   ✓ Workflows: Read and write (optional)
   ```

5. Click **"Generate token"**

6. **COPY THE TOKEN** immediately!

### Step 2: Enable Dependabot in Your Repository

1. Go to your repository settings:
   **https://github.com/HCL1111/Springboot-demo/settings/security_analysis**

2. Find the **"Dependabot"** section

3. Enable these features:
   ```
   ✓ Dependabot alerts
   ✓ Dependabot security updates (recommended)
   ✓ Grouped security updates (optional)
   ```

4. Click **"Enable"** for each

5. **Wait 2-5 minutes** for GitHub to scan your dependencies

### Step 3: Set Environment Variables

#### On Linux / macOS:

```bash
# Add to your ~/.bashrc or ~/.zshrc for persistence
export GITHUB_TOKEN='ghp_your_token_here'
export GITHUB_REPOSITORY='HCL1111/Springboot-demo'

# Or for current session only:
export GITHUB_TOKEN='ghp_your_token_here'
export GITHUB_REPOSITORY='HCL1111/Springboot-demo'
```

#### On Windows PowerShell:

```powershell
# For current session:
$env:GITHUB_TOKEN='ghp_your_token_here'
$env:GITHUB_REPOSITORY='HCL1111/Springboot-demo'

# For persistent (all sessions):
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN','ghp_your_token_here','User')
[System.Environment]::SetEnvironmentVariable('GITHUB_REPOSITORY','HCL1111/Springboot-demo','User')
```

#### On Windows CMD:

```cmd
set GITHUB_TOKEN=ghp_your_token_here
set GITHUB_REPOSITORY=HCL1111/Springboot-demo
```

### Step 4: Validate Your Setup

Run the token validator to check everything is configured correctly:

```bash
python scripts/setup_token.py
```

This will:
- ✅ Validate your token is working
- ✅ Check if you have the required `security_events` scope
- ✅ Verify access to the repository
- ✅ Check if Dependabot is enabled
- ✅ Test Dependabot API access

**Expected output if everything is correct:**
```
================================================================================
VALIDATION SUMMARY
================================================================================
✅ All checks passed! Your token is configured correctly.

You can now run the CVE scanner:
   python scripts/fix_cves.py
```

### Step 5: Run the CVE Scanner

Once validation passes, run the scanner:

```bash
python scripts/fix_cves.py
```

It should now successfully:
1. Access the Dependabot API (no 403 error!)
2. Detect CVE-2024-47554 in commons-io:2.13.0
3. Apply the fix
4. Run tests
5. Generate a report

## Troubleshooting

### Still Getting 403 Errors?

Run the diagnostic:

```bash
python scripts/setup_token.py
```

Check the output for specific issues.

### Common Issues:

#### Issue 1: "Token missing 'security_events' scope"

**Fix**: Recreate your token with the `security_events` scope selected (see Step 1)

#### Issue 2: "Dependabot vulnerability alerts are DISABLED"

**Fix**: Enable Dependabot in repository settings (see Step 2)

#### Issue 3: "Repository not found or not accessible"

**Fix**: 
- Check `GITHUB_REPOSITORY` is set correctly: `owner/repo`
- Ensure token has access to the repository
- For fine-grained tokens, ensure repository is selected

#### Issue 4: "Token is invalid or expired"

**Fix**: Generate a new token (see Step 1)

### Verify Token Manually:

You can also test your token manually with curl:

```bash
# Test basic access
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/user

# Test Dependabot API
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/$GITHUB_REPOSITORY/dependabot/alerts
```

If the second command returns JSON (not 403), your token is configured correctly!

## Why This Happens

### Different Permissions for Different APIs

GitHub's API has different permission requirements:

| API Endpoint | Required Permission |
|--------------|---------------------|
| `/repos/{owner}/{repo}` | `repo` or `public_repo` |
| `/repos/{owner}/{repo}/dependabot/alerts` | `security_events` ⭐ |
| `/repos/{owner}/{repo}/vulnerability-alerts` | `security_events` ⭐ |
| `/graphql` (vulnerabilities) | `repo` + `security_events` |

**The key insight**: Even if you have `repo` access, you need **additional `security_events` permission** for security-related endpoints.

### GitHub Actions vs Personal Tokens

In GitHub Actions workflows:
- The `GITHUB_TOKEN` is automatically created
- Permissions are granted via workflow YAML
- `security-events: read` in workflow = `security_events` scope for personal tokens

For personal use:
- You must **manually create** a token
- You must **explicitly select** the `security_events` scope
- It's easy to miss this scope!

## Summary

**The 403 error on your personal laptop happens because:**

1. ❌ You don't have a token with `security_events` scope
2. ❌ Or Dependabot isn't enabled in your repository
3. ❌ Or the environment variables aren't set

**The fix is:**

1. ✅ Create a Personal Access Token with `security_events` scope
2. ✅ Enable Dependabot in repository settings
3. ✅ Set `GITHUB_TOKEN` and `GITHUB_REPOSITORY` environment variables
4. ✅ Run `python scripts/setup_token.py` to validate
5. ✅ Run `python scripts/fix_cves.py` to scan for CVEs

## Next Steps

After fixing your setup:

1. ✅ The CVE scanner will work on your personal laptop
2. ✅ You'll be able to detect vulnerabilities via Dependabot API
3. ✅ Fallback methods (OSV, built-in DB) still available as backup
4. ✅ All three detection tiers will work correctly

The fallback mechanisms we added earlier are still valuable - they ensure the scanner works even if:
- Dependabot API is temporarily unavailable
- You're in a restricted network
- You want to run offline

But for normal personal use, **the Dependabot API should now work with your properly configured token!**
