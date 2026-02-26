# CVE Scanner GitHub Actions Testing Guide

This guide explains how to test the CVE Scanner GitHub Actions workflow.

## Overview

The CVE Scanner workflow (`cve-scanner.yml`) is configured to:
- Run automatically every Monday at 00:00 UTC
- Can be triggered manually via workflow_dispatch
- Scans Gradle dependencies for CVEs
- Automatically fixes vulnerabilities
- Creates Pull Requests with the fixes

## Testing the Workflow

### Option 1: Manual Workflow Trigger (Recommended)

1. **Navigate to Actions Tab**
   - Go to your GitHub repository
   - Click on the "Actions" tab

2. **Select CVE Scanner Workflow**
   - In the left sidebar, click "CVE Scanner and Auto-Fix"

3. **Run Workflow**
   - Click "Run workflow" button (top right)
   - Select the branch (typically `master` or `main`)
   - Click the green "Run workflow" button

4. **Monitor Execution**
   - Click on the running workflow to see real-time logs
   - Watch each step complete:
     - ✅ Checkout repository
     - ✅ Set up JDK 17
     - ✅ Set up Python 3.11
     - ✅ Install Python dependencies
     - ✅ Run CVE Scanner and Fixer
     - ✅ Upload CVE Report (if vulnerabilities found)

### Option 2: Test with Vulnerable Dependency

To verify the scanner can actually detect and fix CVEs:

1. **Create a Test Branch**
   ```bash
   git checkout -b test/cve-scanner
   ```

2. **Introduce a Vulnerable Dependency**
   Edit `build.gradle` and replace:
   ```gradle
   runtimeOnly 'com.h2database:h2:2.4.240'
   ```
   With a vulnerable version:
   ```gradle
   runtimeOnly 'com.h2database:h2:2.1.214'
   ```

3. **Commit and Push**
   ```bash
   git add build.gradle
   git commit -m "test: Add vulnerable dependency for CVE scanner testing"
   git push origin test/cve-scanner
   ```

4. **Trigger Workflow**
   - Go to Actions tab
   - Select "CVE Scanner and Auto-Fix"
   - Click "Run workflow"
   - Select `test/cve-scanner` branch
   - Run the workflow

5. **Verify Results**
   - Scanner should detect H2 2.1.214 as vulnerable
   - Scanner should update it to a secure version (e.g., 2.3.232)
   - Build and tests should pass
   - A Pull Request should be created (if permissions allow)
   - CVE report should be uploaded as artifact

6. **Cleanup**
   ```bash
   git checkout master
   git branch -D test/cve-scanner
   git push origin --delete test/cve-scanner
   ```

### Option 3: Local Testing

Test the Python script locally before running in CI/CD:

```bash
# Install dependencies
pip install requests

# Run the test suite first
python scripts/test_cve_scanner.py

# Run the scanner manually
python scripts/fix_cves.py
```

## Expected Behavior

### When Vulnerabilities Are Found

1. **Scanner Output**
   ```
   ================================================================================
   CVE Vulnerability Scanner and Fixer
   ================================================================================
   
   Step 1: Scanning for vulnerabilities...
   Found X open Dependabot alerts
   
   Step 2: Analyzing vulnerabilities...
   Found X unique vulnerabilities:
     - package:name: CVE-XXXX-XXXXX (Severity: High)
       Current: 1.0.0, Fix: 1.0.1
   
   Step 3: Found X vulnerabilities. Applying fixes...
   ✅ Updated package:name to 1.0.1
   
   Step 4: Running Gradle build and tests...
   Build successful!
   All tests passed!
   
   Step 5: Generating summary report...
   📄 Report generated: CVE_FIX_REPORT.md
   
   Step 6: Creating Pull Request...
   ✅ Pull Request created successfully
   
   ================================================================================
   ✅ CVE fixes completed successfully!
   ================================================================================
   ```

2. **Artifacts Generated**
   - `CVE_FIX_REPORT.md` - Detailed report of fixes
   - Updated `build.gradle` with patched versions
   - Pull Request with security updates

3. **Pull Request Created**
   - Title: `[Security] Fix X CVE vulnerability(ies)`
   - Contains detailed information about each fix
   - Includes verification that build and tests pass

### When No Vulnerabilities Are Found

```
================================================================================
CVE Vulnerability Scanner and Fixer
================================================================================

Step 1: Scanning for vulnerabilities...
Step 2: Analyzing vulnerabilities...
No vulnerabilities detected.

✅ No vulnerabilities found! All dependencies are secure.
```

## Monitoring Workflow Execution

### View Workflow Runs

1. Go to **Actions** tab
2. Click on **CVE Scanner and Auto-Fix** workflow
3. See history of all runs with status:
   - ✅ Success - No vulnerabilities or fixes applied successfully
   - ❌ Failure - Build failed or scanner error
   - ⚪ Skipped - Workflow was cancelled

### Download Artifacts

After a run completes:
1. Click on the workflow run
2. Scroll to **Artifacts** section at the bottom
3. Download:
   - `cve-fix-report` - The CVE fix report markdown
   - `dependency-check-report` - Additional security scan results (if available)

### View Logs

Click on any step to see detailed logs:
- **Set up Python** - Python installation logs
- **Install Python dependencies** - pip installation logs
- **Run CVE Scanner and Fixer** - Complete scanner output
- **Upload CVE Report** - Artifact upload status

## Workflow Configuration

The workflow is defined in `.github/workflows/cve-scanner.yml`:

```yaml
name: CVE Scanner and Auto-Fix

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday at 00:00 UTC
  workflow_dispatch:      # Manual trigger

permissions:
  contents: write         # To commit changes
  pull-requests: write    # To create PRs
  security-events: read   # To read Dependabot alerts
```

## Troubleshooting

### Workflow Doesn't Trigger

**Problem:** Manual trigger button not visible
**Solution:** Ensure you have write access to the repository

### Scanner Can't Access Dependabot Alerts

**Problem:** `Could not fetch Dependabot alerts (status 403)`
**Solution:** This is normal. Scanner falls back to manual Maven Central checking

### Build Fails After Fixes

**Problem:** Build or tests fail after dependency updates
**Solution:** 
- Review the build logs in the workflow
- Check if the new version has breaking changes
- May need manual intervention for complex dependency conflicts

### PR Creation Fails

**Problem:** `Error creating PR: Permission denied`
**Solution:**
- Ensure workflow has `pull-requests: write` permission
- Check if `GITHUB_TOKEN` has sufficient permissions
- In forks, PRs may need to be created manually

## Environment Variables

The workflow uses these environment variables:

- `GITHUB_TOKEN` - Automatically provided by GitHub Actions
- `GITHUB_REPOSITORY` - Automatically set to `owner/repo`

## Best Practices

1. **Test Locally First** - Run `python scripts/test_cve_scanner.py` before pushing
2. **Review PRs Carefully** - Always review auto-generated PRs before merging
3. **Check Breaking Changes** - Verify dependency updates don't break functionality
4. **Monitor Regularly** - Check workflow runs weekly
5. **Keep Scanner Updated** - Update the scanner script as needed

## Verification Checklist

After running the workflow, verify:

- [ ] Workflow completed successfully
- [ ] Python 3.11 was set up correctly
- [ ] Python dependencies (requests) were installed
- [ ] CVE scanner ran without errors
- [ ] If vulnerabilities found:
  - [ ] CVE report was generated
  - [ ] build.gradle was updated
  - [ ] Build and tests passed
  - [ ] PR was created (or attempted)
- [ ] If no vulnerabilities:
  - [ ] Scanner reported "No vulnerabilities found"
  - [ ] No changes were made to build.gradle

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Dispatch Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch)
- [GitHub Dependabot](https://docs.github.com/en/code-security/dependabot)
- [Scanner Script Documentation](./scripts/README.md)

## Support

If you encounter issues:
1. Check the workflow logs for detailed error messages
2. Run the test suite locally: `python scripts/test_cve_scanner.py`
3. Review the scanner documentation in `scripts/README.md`
4. Check recent commits for any configuration changes
