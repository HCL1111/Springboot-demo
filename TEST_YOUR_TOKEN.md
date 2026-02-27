# Testing Your GitHub Token

## ⚠️ SECURITY WARNING

**YOUR TOKEN HAS BEEN EXPOSED!**

The token `ghp_9OZL**********************LUEl` was shared in plain text. You should:

1. **IMMEDIATELY REVOKE THIS TOKEN** at: https://github.com/settings/tokens
2. **Generate a new token** (see guide below)
3. **NEVER share tokens** in chat, code, or public places

GitHub may have already automatically revoked this token when it was detected in this conversation.

---

## How to Safely Use Your Token

### Step 1: Generate a NEW Token (the old one is compromised)

1. Go to: https://github.com/settings/tokens/new

2. Configure the token:
   - **Note**: `CVE Scanner for Springboot-demo`
   - **Expiration**: 90 days (recommended)
   - **Select scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `security_events` (Read security events) ⭐ **REQUIRED**
     - ✅ `workflow` (Update GitHub Action workflows) - optional

3. Click **"Generate token"**

4. **Copy the token immediately** - you won't see it again!

### Step 2: Configure Token on Your Local Machine

**NEVER put tokens in code files!** Use environment variables instead.

#### On Linux/macOS:

```bash
# Set for current terminal session
export GITHUB_TOKEN='your_new_token_here'
export GITHUB_REPOSITORY='HCL1111/Springboot-demo'

# Or add to ~/.bashrc or ~/.zshrc for persistence:
echo 'export GITHUB_TOKEN="your_new_token_here"' >> ~/.bashrc
echo 'export GITHUB_REPOSITORY="HCL1111/Springboot-demo"' >> ~/.bashrc
source ~/.bashrc
```

#### On Windows PowerShell:

```powershell
# Set for current session
$env:GITHUB_TOKEN='your_new_token_here'
$env:GITHUB_REPOSITORY='HCL1111/Springboot-demo'

# Set permanently (for all sessions):
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN','your_new_token_here','User')
[System.Environment]::SetEnvironmentVariable('GITHUB_REPOSITORY','HCL1111/Springboot-demo','User')
```

#### On Windows CMD:

```cmd
set GITHUB_TOKEN=your_new_token_here
set GITHUB_REPOSITORY=HCL1111/Springboot-demo
```

### Step 3: Validate Your Token

Run the validator to check if your token is configured correctly:

```bash
cd /path/to/Springboot-demo
python scripts/setup_token.py
```

**Expected Output (Success):**

```
================================================================================
GitHub Token Validator for CVE Scanner
================================================================================

🔍 Validating token for repository: HCL1111/Springboot-demo

1️⃣  Validating GitHub token...
   ✅ Token valid - Authenticated as: YourUsername
   Token scopes: repo, security_events
   ✅ Has security_events scope

2️⃣  Validating repository access...
   ✅ Repository accessible: HCL1111/Springboot-demo
   Private: false
   Permissions: admin=true, push=true, pull=true

3️⃣  Checking if Dependabot is enabled...
   ✅ Dependabot vulnerability alerts are ENABLED

4️⃣  Testing Dependabot alerts API access...
   ✅ Dependabot API accessible
   Found X Dependabot alert(s)
   Open alerts: Y

================================================================================
VALIDATION SUMMARY
================================================================================
✅ All checks passed! Your token is configured correctly.

You can now run the CVE scanner:
   python scripts/fix_cves.py
```

### Step 4: Test the CVE Scanner

Once validation passes, run the CVE scanner:

```bash
python scripts/fix_cves.py
```

This will:
1. ✅ Scan for vulnerabilities using Dependabot API
2. ✅ Detect CVE-2024-47554 in commons-io:2.13.0
3. ✅ Automatically update to safe version
4. ✅ Run Gradle build to verify
5. ✅ Generate CVE_FIX_REPORT.md
6. ✅ Create a Pull Request with the fix

### Step 5: Verify the Results

Check that:

1. **The scanner runs without 403 errors**
2. **Vulnerabilities are detected**
3. **build.gradle is updated**
4. **Gradle build succeeds**
5. **A Pull Request is created**

---

## Troubleshooting

### Issue: "Token invalid or expired"

**Solution**: The old token was revoked. Generate a new one (Step 1).

### Issue: "Missing 'security_events' scope"

**Solution**: When creating the token, make sure to check the `security_events` checkbox.

### Issue: "Dependabot alerts not available"

**Solution**: Enable Dependabot at:
https://github.com/HCL1111/Springboot-demo/settings/security_analysis

### Issue: "Repository not found"

**Solution**: Check that `GITHUB_REPOSITORY` is set to `HCL1111/Springboot-demo`

---

## Complete Test Flow Example

Here's a complete example of testing on your local machine:

```bash
# 1. Navigate to repository
cd ~/Springboot-demo

# 2. Set environment variables (use YOUR new token!)
export GITHUB_TOKEN='ghp_YOUR_NEW_TOKEN_HERE'
export GITHUB_REPOSITORY='HCL1111/Springboot-demo'

# 3. Verify environment
echo "Token set: $(echo $GITHUB_TOKEN | head -c 10)..."
echo "Repository: $GITHUB_REPOSITORY"

# 4. Validate token
python scripts/setup_token.py

# 5. If validation passes, run CVE scanner
python scripts/fix_cves.py

# 6. Check the results
cat CVE_FIX_REPORT.md
git status
```

---

## Security Best Practices

### ✅ DO:
- Store tokens in environment variables
- Use fine-grained tokens with minimal permissions
- Set token expiration (30-90 days)
- Revoke tokens when no longer needed
- Use different tokens for different purposes

### ❌ DON'T:
- Commit tokens to Git repositories
- Share tokens in chat or email
- Use tokens in code files
- Give tokens more permissions than needed
- Use tokens without expiration

---

## Next Steps

1. **Revoke the exposed token**: https://github.com/settings/tokens
2. **Generate a new token** with `security_events` scope
3. **Set it as an environment variable** (not in code!)
4. **Run the validator**: `python scripts/setup_token.py`
5. **Run the CVE scanner**: `python scripts/fix_cves.py`

The CVE scanner should now work perfectly on your personal laptop! 🎉
