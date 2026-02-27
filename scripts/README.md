# CVE Scanner and Fixer

This directory contains automation scripts for security vulnerability management.

## Quick Start for Personal Use

**Getting 403 errors?** Start here:

```bash
# 1. Validate your GitHub token setup
python scripts/setup_token.py

# 2. Follow the interactive guide to fix any issues

# 3. Once validation passes, run the CVE scanner
python scripts/fix_cves.py
```

See **[FIXING_403_FOR_PERSONAL_USE.md](../FIXING_403_FOR_PERSONAL_USE.md)** for complete setup guide.

## Files

### `setup_token.py` ⭐ NEW

**Interactive token validator and setup guide for personal GitHub accounts.**

This tool helps you configure your GitHub Personal Access Token with the correct permissions to avoid 403 errors.

**Usage:**

```bash
python scripts/setup_token.py
```

**What it does:**
- ✅ Validates your GitHub token
- ✅ Checks for required `security_events` permission
- ✅ Verifies repository access
- ✅ Tests Dependabot API connectivity
- ✅ Provides step-by-step setup guidance if issues are found

**When to use:**
- When you get 403 Forbidden errors
- When setting up the scanner for the first time on your personal laptop
- To troubleshoot token permission issues

### `fix_cves.py`

Automated CVE vulnerability scanner and fixer for Gradle projects.

**Features:**
- Scans dependencies for known CVEs using **multi-tier detection**:
  1. **Primary**: GitHub Dependabot API (when available)
  2. **Fallback 1**: OSV (Open Source Vulnerabilities) API
  3. **Fallback 2**: Built-in known CVE database
- Automatically updates vulnerable dependencies to secure versions
- Runs Gradle build and tests to verify fixes
- Generates detailed CVE fix reports
- Creates Pull Requests with security updates

**Detection Methods:**

The scanner uses a three-tier fallback approach to ensure vulnerability detection even in restricted network environments:

1. **GitHub Dependabot API** (Primary)
   - Most accurate and up-to-date vulnerability data
   - Requires `GITHUB_TOKEN` with `security_events` read permission
   - Requires Dependabot alerts enabled on the repository

2. **OSV API** (Fallback 1)
   - Uses Google's Open Source Vulnerabilities database
   - Queries api.osv.dev for each dependency
   - Works without GitHub authentication

3. **Built-in Known CVE Database** (Fallback 2)
   - Local database of common, well-known CVEs
   - Works offline and in restricted environments
   - Updated periodically with critical vulnerabilities
   - Current coverage includes: commons-io, h2, log4j, jackson, commons-text

**Important:** The scanner will attempt all three methods in order and use the first one that successfully detects vulnerabilities. This ensures detection works even when:
- GitHub API is unavailable or blocked
- Network restrictions prevent external API access
- Running in air-gapped or offline environments

**Usage:**

```bash
# Run the scanner (will use best available detection method)
python scripts/fix_cves.py

# With GitHub token for Dependabot integration (recommended for best results)
GITHUB_TOKEN=your_token GITHUB_REPOSITORY=owner/repo python scripts/fix_cves.py

# Without GitHub token (will use OSV API or built-in database)
python scripts/fix_cves.py
```

**Detection Hierarchy:**
1. If `GITHUB_TOKEN` and `GITHUB_REPOSITORY` are set → Uses Dependabot API
2. If Dependabot fails or unavailable → Tries OSV API
3. If OSV fails or network blocked → Uses built-in known CVE database

**Environment Variables:**
- `GITHUB_TOKEN`: GitHub token with `security_events` read permission (optional but recommended)
- `GITHUB_REPOSITORY`: Repository in format `owner/repo` (optional but recommended)

**Output:**
- `CVE_FIX_REPORT.md`: Detailed report of vulnerabilities and fixes
- Updated `build.gradle`: With patched dependency versions

## GitHub Actions Integration

The CVE scanner is automatically triggered by the `cve-scanner.yml` workflow:

- **Schedule**: Runs every Monday at 00:00 UTC
- **Manual Trigger**: Can be triggered manually via workflow_dispatch
- **Automatic PRs**: Creates pull requests when vulnerabilities are fixed

## How It Works

1. **Scan**: Tries multiple detection methods in order:
   - **Primary**: Fetches vulnerability alerts from GitHub Dependabot API
     * Checks all alert states (open, dismissed, etc.)
     * Filters out only truly "fixed" alerts
     * Matches alerts against current dependencies in build.gradle
   - **Fallback 1**: Queries OSV (Open Source Vulnerabilities) API
     * Sends each dependency to api.osv.dev for vulnerability lookup
     * Extracts CVE information and fixed versions
   - **Fallback 2**: Checks against built-in known CVE database
     * Matches dependencies against curated list of common CVEs
     * Includes critical vulnerabilities for popular libraries
2. **Analyze**: Identifies vulnerable packages and determines safe versions
3. **Fix**: Automatically updates `build.gradle` with patched versions
4. **Verify**: Runs `./gradlew clean build` to ensure fixes don't break the build
5. **Report**: Generates a detailed markdown report with CVE information
6. **PR**: Creates a pull request with all changes for review

**Design Principles:**
- Prioritizes most accurate sources (Dependabot) but ensures detection works offline
- Multiple fallback layers prevent detection failure due to network issues
- Built-in database covers common, critical CVEs for popular libraries
- All detected vulnerabilities include fix version information

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

### `test_cve_scanner.py`

Comprehensive test suite for the CVE scanner.

**Features:**
- Tests vulnerability detection capability
- Verifies automatic fix application
- Validates CVE report generation
- Ensures build passes after fixes
- Tests no-vulnerability scenario

**Usage:**

```bash
# Run the test suite
python scripts/test_cve_scanner.py
```

**Test Coverage:**
1. ✅ Scanner tries multiple detection methods (Dependabot → OSV → Known CVEs)
2. ✅ Scanner works even when APIs are unavailable
3. ✅ Scanner detects vulnerabilities using fallback methods
4. ✅ Scanner provides clear status messages for each detection method
5. ✅ Scanner correctly handles secure dependencies

The test suite automatically:
- Creates a backup of build.gradle
- Introduces a known vulnerable dependency (commons-io 2.13.0 with CVE-2024-47554)
- Runs the scanner to verify multi-tier detection
- Verifies scanner can detect vulnerabilities via built-in database
- Tests the no-vulnerability case
- Restores the original state

**Note:** The tests verify that the scanner has resilient fallback mechanisms and can detect vulnerabilities even when external APIs (Dependabot, OSV) are unavailable.

### `trigger-workflow.sh`

Interactive Bash script to trigger GitHub Actions workflows on specific branches using GitHub CLI.

**Use Case:**
When a branch doesn't appear in the GitHub UI dropdown for manual workflow triggers, this script provides a reliable alternative.

**Features:**
- Interactive menu to select workflows
- Supports triggering single or multiple workflows
- Verifies branch existence before triggering
- Shows recent workflow runs after triggering
- User-friendly with step-by-step prompts

**Usage:**

```bash
# Trigger workflow on the default branch (copilot/add-dependency-vulnerability)
./scripts/trigger-workflow.sh

# Trigger workflow on a custom branch
./scripts/trigger-workflow.sh my-custom-branch
```

**Prerequisites:**
- GitHub CLI (`gh`) must be installed
- Authenticated with GitHub (`gh auth login`)

**Installation:**

```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
scoop install gh
```

### `trigger_workflow_api.py`

Python script to trigger GitHub Actions workflows via the GitHub REST API.

**Use Case:**
When branches don't appear in the GitHub UI or when you need programmatic workflow triggering without GitHub CLI.

**Features:**
- Direct API-based workflow triggering
- List all available workflows
- Verify branch existence
- Support for multiple workflows in one command
- Detailed success/failure reporting
- Works anywhere Python is available

**Usage:**

```bash
# Install requirements
pip install requests

# Set GitHub token
export GITHUB_TOKEN=your_github_token_here

# Trigger a single workflow
python scripts/trigger_workflow_api.py \
  --workflow cve-scanner.yml \
  --branch copilot/add-dependency-vulnerability

# Trigger multiple workflows
python scripts/trigger_workflow_api.py \
  --workflow cve-scanner.yml \
  --workflow codeql.yml \
  --branch my-branch

# List all workflows
python scripts/trigger_workflow_api.py --list-workflows

# Use custom repository
python scripts/trigger_workflow_api.py \
  --repo owner/repo \
  --workflow my-workflow.yml \
  --branch main \
  --token your_token
```

**GitHub Token:**
Create a personal access token at: https://github.com/settings/tokens
Required scopes: `repo`, `workflow`

## Workflow Branch Availability

If you're having trouble selecting a branch when manually triggering workflows in the GitHub UI, see:
- **`WORKFLOW_BRANCH_AVAILABILITY.md`** in the root directory for detailed troubleshooting
- **`trigger-workflow.sh`** or **`trigger_workflow_api.py`** for alternative triggering methods
- **`.github/workflows/list-workflow-branches.yml`** to diagnose which branches have workflows

## Requirements

- Python 3.8+
- `requests` library (for Python scripts)
- Git
- Gradle
- GitHub CLI (for trigger-workflow.sh, optional for other scripts)
