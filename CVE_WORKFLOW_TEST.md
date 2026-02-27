# CVE Workflow Testing Guide

## Overview
This document explains how to test the automated CVE detection and fixing workflow in this repository.

## Test Scenario

### What Was Added
A **vulnerable dependency** has been intentionally added to `build.gradle`:
- **Dependency**: `commons-io:commons-io:2.13.0`
- **Vulnerability**: CVE-2024-47554 (Uncontrolled Resource Consumption / DoS)
- **Description**: Vulnerability in XmlStreamReader class that can consume excessive CPU when processing malicious XML
- **Severity**: Medium
- **Fixed In**: Apache Commons IO 2.14.0 or higher

### How to Test the CVE Workflow

1. **Merge this PR to master branch**
   - This PR contains the vulnerable dependency (commons-io:2.13.0)
   - The dependency is intentionally NOT fixed in this PR

2. **Manually trigger the CVE Scanner workflow**
   - Go to Actions tab in GitHub
   - Select "CVE Scanner and Auto-Fix" workflow
   - Click "Run workflow" button
   - Select the master branch
   - Click "Run workflow" to start

3. **Expected Behavior**
   The Python script (`scripts/fix_cves.py`) should:
   - Detect the vulnerability using GitHub Dependabot API
   - Identify CVE-2024-47554 in commons-io:2.13.0
   - Automatically update to a safe version (2.14.0 or higher)
   - Run Gradle build and tests to verify the fix
   - Generate a CVE_FIX_REPORT.md file
   - Create a new PR with the fix

4. **Verification Steps**
   - Check workflow execution logs for vulnerability detection
   - Verify a new PR is created with the fix
   - Review the CVE_FIX_REPORT.md artifact
   - Confirm build.gradle is updated to use a safe version
   - Ensure Gradle build passes in the fix PR

## Technical Details

### Vulnerability Information
```
CVE ID: CVE-2024-47554
Package: commons-io:commons-io
Vulnerable Version: 2.13.0 (and earlier versions 2.0 - 2.13.x)
Fixed Version: 2.14.0+
CVSS Score: Medium
Attack Vector: Network (requires malicious XML input)
```

### Expected Fix
The CVE scanner should update the dependency from:
```gradle
implementation 'commons-io:commons-io:2.13.0'
```

To:
```gradle
implementation 'commons-io:commons-io:2.14.0'  // or higher
```

## Success Criteria

The workflow test is successful if:
1. ✅ The CVE scanner detects CVE-2024-47554
2. ✅ The scanner automatically updates commons-io to 2.14.0 or higher
3. ✅ Gradle build passes after the fix
4. ✅ A PR is created with the fix
5. ✅ CVE_FIX_REPORT.md is generated with details

## Cleanup

After testing is complete:
1. Review and merge the auto-generated fix PR
2. Delete the test branch if no longer needed
3. Optionally remove this test documentation file

## Notes

- This is a controlled test to validate the automated CVE detection and fixing pipeline
- The vulnerable dependency was intentionally added for testing purposes
- The CVE scanner relies on GitHub Dependabot API (no hardcoded patterns)
- The workflow can be triggered manually or runs automatically on a schedule
