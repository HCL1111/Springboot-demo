# CVE Scanner Testing Instructions

This document provides step-by-step instructions to manually test the CVE scanner workflow.

## Overview
This repository now contains **9 deliberate security vulnerabilities** in its dependencies. These vulnerabilities were intentionally added to test the automated CVE scanner and fixer workflow.

## How to Test the CVE Scanner

### Option 1: Manual Workflow Trigger (Recommended)

1. **Navigate to GitHub Actions**
   - Go to the repository on GitHub
   - Click on the "Actions" tab
   - Find the "CVE Scanner and Auto-Fix" workflow in the left sidebar

2. **Trigger the Workflow**
   - Click on "CVE Scanner and Auto-Fix"
   - Click the "Run workflow" button (top right)
   - Select the branch containing the vulnerabilities (the current branch with these changes)
   - Click the green "Run workflow" button

3. **Monitor the Workflow**
   - The workflow will start running
   - Click on the workflow run to see live progress
   - It should complete in 3-5 minutes

4. **Review the Results**
   - Check the workflow run summary for detected vulnerabilities
   - Download the CVE report artifact if available
   - Look for a new Pull Request created by the workflow

5. **Verify the Pull Request**
   - A new PR should be created with title like "Fix CVE vulnerabilities"
   - The PR should update all 9 vulnerable dependencies to secure versions
   - Review the changes in build.gradle
   - The PR description should list all detected and fixed CVEs

### Option 2: Wait for Scheduled Run

The workflow is scheduled to run automatically every Monday at 00:00 UTC. If you prefer, you can wait for the next scheduled run.

## Expected Vulnerabilities to be Detected

The CVE scanner should detect the following vulnerabilities:

| Dependency | Vulnerable Version | CVE | Severity |
|------------|-------------------|-----|----------|
| Apache Tomcat | 10.1.5 | CVE-2023-42795 | High |
| Logback | 1.2.0 | CVE-2021-42550 | High |
| H2 Database | 2.1.210 | CVE-2022-45868 | Critical |
| Log4j | 2.14.1 | CVE-2021-44228 (Log4Shell) | Critical |
| Jackson | 2.12.0 | CVE-2020-36518 | Medium-High |
| Commons Text | 1.9 | CVE-2022-42889 (Text4Shell) | Critical |
| Spring Security | 5.5.0 | CVE-2021-22112 | High |
| Lombok | 1.18.20 | Various | Medium |
| JSON Smart | 2.4.7 | CVE-2023-1370 | Medium |

## Expected Workflow Behavior

### What the CVE Scanner Should Do:

1. **Scan Phase**
   - Analyze build.gradle dependencies
   - Query GitHub Dependabot API for known vulnerabilities
   - Check Maven Central for vulnerability information

2. **Analysis Phase**
   - Identify all vulnerable dependencies
   - Determine the latest secure versions
   - Generate a list of required updates

3. **Fix Phase**
   - Automatically update build.gradle with secure versions
   - Update version numbers in the ext block and dependency declarations

4. **Verification Phase**
   - Run `./gradlew clean build --no-daemon`
   - Ensure all tests pass with the updated dependencies
   - Verify the build is successful

5. **Reporting Phase**
   - Generate CVE_FIX_REPORT.md with detailed information
   - Create a summary of all fixes applied

6. **PR Creation Phase**
   - Create a new branch (e.g., `fix/cve-vulnerabilities-YYYY-MM-DD`)
   - Commit the changes
   - Create a Pull Request with comprehensive description
   - Include all CVEs fixed and version updates

## Verifying the Fix

After the CVE scanner creates a PR:

1. **Review the PR Changes**
   - All 9 vulnerable dependencies should be updated
   - Version numbers should match or exceed these minimums:
     - Tomcat: 10.1.52+
     - Logback: 1.5.32+
     - H2: 2.4.240+
     - Log4j: 2.25.3+
     - Jackson: 2.21.1+
     - Commons Text: 1.15.0+
     - Spring Security: 6.5.8+
     - Lombok: 1.18.42+
     - JSON Smart: 2.6.0+

2. **Check the Build Status**
   - The PR should trigger CI builds
   - All builds should pass
   - Tests should pass

3. **Review the CVE Report**
   - Download the CVE_FIX_REPORT.md artifact
   - Verify all vulnerabilities are listed
   - Check that each fix is documented

## Troubleshooting

### If the workflow fails:
- Check the workflow logs in GitHub Actions
- Look for error messages in the Python script execution
- Verify that the GITHUB_TOKEN has sufficient permissions
- Ensure the repository settings allow workflow PR creation

### If vulnerabilities are not detected:
- Wait a few hours for GitHub's dependency graph to update
- Check if Dependabot is enabled on the repository
- Verify the GITHUB_TOKEN environment variable is set

### If the build fails after fixes:
- Check for version conflicts
- Review the Gradle dependency resolution
- Look for incompatible dependency combinations

## Cleanup After Testing

Once testing is complete:

1. **Merge the Fix PR**
   - Review and approve the PR created by the CVE scanner
   - Merge it to update the main branch with secure dependencies

2. **Verify the Main Branch**
   - Ensure the main branch has no remaining vulnerabilities
   - Run the CVE scanner again to confirm

3. **Clean Up Test Documentation** (Optional)
   - You may want to remove VULNERABILITY_TEST.md and this file
   - Keep CVE_FIX_REPORT.md for reference

## Additional Testing

You can also test the CVE scanner with:

```bash
# Run the Python test suite
python scripts/test_cve_scanner.py

# Run the scanner manually (requires Python 3.11+)
pip install requests
python scripts/fix_cves.py
```

## Support

For questions or issues with the CVE scanner:
- Review scripts/README.md for technical details
- Check CVE_SCANNER_SUMMARY.md for capabilities
- See GITHUB_ACTIONS_TESTING.md for workflow configuration
