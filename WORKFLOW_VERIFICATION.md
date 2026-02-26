# GitHub Actions Workflow Verification Guide

## Quick Verification Steps

Follow these steps to verify the CVE scanner is properly configured and working in GitHub Actions:

### Step 1: Navigate to Actions Tab
1. Go to https://github.com/HCL1111/Springboot-demo
2. Click on the "Actions" tab in the top navigation

### Step 2: Locate CVE Scanner Workflow
1. In the left sidebar, look for "CVE Scanner and Auto-Fix"
2. Click on it to see the workflow details

### Step 3: Manual Trigger (Recommended for Testing)
1. Click the "Run workflow" button (top right, next to "This workflow has a workflow_dispatch event trigger")
2. Select the branch you want to test (e.g., "master" or "copilot/configure-github-action-python")
3. Click the green "Run workflow" button

### Step 4: Monitor Execution
1. The workflow run will appear at the top of the runs list
2. Click on it to see real-time logs
3. You should see these steps executing:
   - ✅ Checkout repository
   - ✅ Set up JDK 17
   - ✅ Set up Python (3.11)
   - ✅ Install Python dependencies
   - ✅ Grant execute permission for gradlew
   - ✅ Run CVE Scanner and Fixer
   - ✅ Upload CVE Report
   - ✅ Summary

### Step 5: Verify Python Execution
Click on the "Run CVE Scanner and Fixer" step to expand it and verify:
- Python script starts with the banner:
  ```
  ================================================================================
  CVE Vulnerability Scanner and Fixer
  ================================================================================
  ```
- Steps execute: Scanning → Analyzing → (Fixing if needed) → Building → Reporting
- Expected end message:
  - If vulnerabilities found: `✅ CVE fixes completed successfully!`
  - If no vulnerabilities: `✅ No vulnerabilities found! All dependencies are secure.`

### Step 6: Check Artifacts (if vulnerabilities were found)
1. Scroll to the bottom of the workflow run page
2. Look for "Artifacts" section
3. Download "cve-fix-report" to see the detailed CVE report

### Step 7: Verify Summary
1. At the top of the workflow run, look for the "Summary" section
2. It should display the CVE scanner results
3. Check that it shows either:
   - Details of fixes applied, OR
   - "No vulnerabilities found" message

## Expected Output Examples

### When No Vulnerabilities Found (Current State)
```
Step 1: Scanning for vulnerabilities...
Checking GitHub Dependabot alerts...
⚠️  Could not fetch Dependabot alerts (status 403)
Falling back to manual scanning...
Performing manual CVE check of current dependencies...
Checking 14 dependencies against Maven Central...
Manual scan complete. Found 0 potential issues.

Step 2: Analyzing vulnerabilities...
No vulnerabilities detected.

✅ No vulnerabilities found! All dependencies are secure.
```

### When Vulnerabilities Are Found (Test Scenario)
```
Step 1: Scanning for vulnerabilities...
Found 1 potential issues.

Step 2: Analyzing vulnerabilities...
Found 1 unique vulnerabilities:
  - com.h2database:h2: CVE-XXXX-XXXXX (Severity: High)
    Current: 2.1.214, Fix: 2.3.232

Step 3: Found 1 vulnerabilities. Applying fixes...
✅ Updated com.h2database:h2 to 2.3.232

Step 4: Running Gradle build and tests...
Build successful!
All tests passed!

Step 5: Generating summary report...
📄 Report generated: CVE_FIX_REPORT.md

Step 6: Creating Pull Request...
✅ Pull Request created successfully
```

## Troubleshooting

### Issue: Can't find "Run workflow" button
**Cause:** You don't have write access to the repository
**Solution:** Contact repository owner for permissions

### Issue: Workflow fails at "Set up Python"
**Cause:** Python setup action might be outdated
**Solution:** Check `.github/workflows/cve-scanner.yml` uses `actions/setup-python@v5`

### Issue: "Could not fetch Dependabot alerts (status 403)"
**Status:** ⚠️ Expected - This is normal
**Explanation:** Scanner automatically falls back to Maven Central API
**Action:** No action required

### Issue: Build fails after applying fixes
**Cause:** Dependency update may have breaking changes
**Solution:** Review the build logs, check dependency release notes, may need manual fix

## Quick Checklist

Use this checklist when verifying the workflow:

- [ ] Actions tab accessible
- [ ] "CVE Scanner and Auto-Fix" workflow visible
- [ ] "Run workflow" button clickable
- [ ] Workflow starts when triggered
- [ ] Python 3.11 setup completes
- [ ] pip install requests completes
- [ ] CVE scanner script executes
- [ ] Appropriate message displayed (vulnerabilities found or not found)
- [ ] If vulnerabilities found: build runs and passes
- [ ] Summary section shows results
- [ ] Artifacts uploaded (if applicable)

## Automated Schedule

The workflow is also configured to run automatically:
- **Schedule:** Every Monday at 00:00 UTC
- **Next scheduled run:** Check the Actions tab for upcoming scheduled runs

## Additional Verification

### Local Testing
You can test the same Python code locally before pushing:

```bash
# Run test suite
python scripts/test_cve_scanner.py

# Run scanner directly
python scripts/fix_cves.py
```

### Verify Workflow File
Check the workflow configuration:
```bash
cat .github/workflows/cve-scanner.yml
```

Look for:
- `python-version: '3.11'` - Python version
- `python scripts/fix_cves.py` - Script execution
- `workflow_dispatch:` - Manual trigger enabled

## Success Indicators

The workflow is working correctly if:
- ✅ Workflow completes with green checkmark
- ✅ All steps show green checkmarks
- ✅ "Run CVE Scanner and Fixer" step shows scanner output
- ✅ Summary shows appropriate message
- ✅ No errors in logs (warnings about Dependabot API are OK)

## Documentation References

- Full testing guide: `GITHUB_ACTIONS_TESTING.md`
- Scanner documentation: `scripts/README.md`
- Complete summary: `CVE_SCANNER_SUMMARY.md`

---

**Last Updated:** 2026-02-26
**Workflow File:** `.github/workflows/cve-scanner.yml`
**Python Script:** `scripts/fix_cves.py`
