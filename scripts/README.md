# CVE Scanner and Fixer

This directory contains automation scripts for security vulnerability management.

## Files

### `fix_cves.py`

Automated CVE vulnerability scanner and fixer for Gradle projects.

**Features:**
- Scans dependencies for known CVEs using GitHub Dependabot API
- Automatically updates vulnerable dependencies to secure versions
- Runs Gradle build and tests to verify fixes
- Generates detailed CVE fix reports
- Creates Pull Requests with security updates

**Usage:**

```bash
# Run the scanner
python scripts/fix_cves.py

# Run with GitHub token for Dependabot integration
GITHUB_TOKEN=your_token GITHUB_REPOSITORY=owner/repo python scripts/fix_cves.py
```

**Environment Variables:**
- `GITHUB_TOKEN`: GitHub token for API access (optional, for Dependabot alerts)
- `GITHUB_REPOSITORY`: Repository in format `owner/repo` (optional)
- `NVD_API_KEY`: NVD API key for OWASP Dependency-Check (optional)

**Output:**
- `CVE_FIX_REPORT.md`: Detailed report of vulnerabilities and fixes
- Updated `build.gradle`: With patched dependency versions

## GitHub Actions Integration

The CVE scanner is automatically triggered by the `cve-scanner.yml` workflow:

- **Schedule**: Runs every Monday at 00:00 UTC
- **Manual Trigger**: Can be triggered manually via workflow_dispatch
- **Automatic PRs**: Creates pull requests when vulnerabilities are fixed

## How It Works

1. **Scan**: Checks dependencies against GitHub Dependabot alerts or Maven Central
2. **Analyze**: Identifies vulnerable packages and determines safe versions
3. **Fix**: Automatically updates `build.gradle` with patched versions
4. **Verify**: Runs `./gradlew clean build` to ensure fixes don't break the build
5. **Report**: Generates a detailed markdown report
6. **PR**: Creates a pull request with all changes for review

## Manual Testing

To test the scanner locally:

```bash
# Install dependencies
pip install requests

# Run scanner
./scripts/fix_cves.py

# Or with Python
python scripts/fix_cves.py
```

The scanner will:
- Check for vulnerabilities
- Display findings
- Apply fixes if vulnerabilities are found
- Run build and tests
- Generate a report

## Requirements

- Python 3.8+
- `requests` library
- Git
- Gradle
- GitHub CLI (for PR creation)
