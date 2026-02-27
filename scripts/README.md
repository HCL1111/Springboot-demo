# CVE Scanner and Fixer

This directory contains automation scripts for security vulnerability management.

## Files

### `fix_cves.py`

Automated CVE vulnerability scanner and fixer for Gradle projects.

**Features:**
- Scans dependencies for known CVEs using **GitHub Dependabot API only**
- **Does NOT use hardcoded vulnerability patterns** - relies entirely on Dependabot
- Automatically updates vulnerable dependencies to secure versions suggested by Dependabot
- Runs Gradle build and tests to verify fixes
- Generates detailed CVE fix reports
- Creates Pull Requests with security updates

**Important:** This scanner requires GitHub Dependabot API access to function. It does not use hardcoded CVE databases or patterns. Ensure:
- Dependabot alerts are enabled for your repository
- The `GITHUB_TOKEN` has `security_events` read permission
- The repository has Dependabot configured to scan dependencies

**Usage:**

```bash
# Run the scanner
python scripts/fix_cves.py

# Run with GitHub token for Dependabot integration (REQUIRED)
GITHUB_TOKEN=your_token GITHUB_REPOSITORY=owner/repo python scripts/fix_cves.py
```

**Note:** Without valid GitHub credentials with Dependabot API access, the scanner will report an error and exit. It does not fall back to hardcoded vulnerability detection.

**Environment Variables:**
- `GITHUB_TOKEN`: GitHub token with `security_events` read permission (**REQUIRED**)
- `GITHUB_REPOSITORY`: Repository in format `owner/repo` (**REQUIRED**)

**Note:** Both environment variables are required for the scanner to work. The scanner relies exclusively on GitHub Dependabot API and will not function without proper API access.

**Output:**
- `CVE_FIX_REPORT.md`: Detailed report of vulnerabilities and fixes
- Updated `build.gradle`: With patched dependency versions

## GitHub Actions Integration

The CVE scanner is automatically triggered by the `cve-scanner.yml` workflow:

- **Schedule**: Runs every Monday at 00:00 UTC
- **Manual Trigger**: Can be triggered manually via workflow_dispatch
- **Automatic PRs**: Creates pull requests when vulnerabilities are fixed

## How It Works

1. **Scan**: Fetches vulnerability alerts from GitHub Dependabot API
   - Checks all alert states (open, dismissed, etc.)
   - Filters out only truly "fixed" alerts
   - Matches alerts against current dependencies in build.gradle
2. **Analyze**: Identifies vulnerable packages from Dependabot data and determines safe versions
3. **Fix**: Automatically updates `build.gradle` with patched versions from Dependabot
4. **Verify**: Runs `./gradlew clean build` to ensure fixes don't break the build
5. **Report**: Generates a detailed markdown report with CVE information from Dependabot
6. **PR**: Creates a pull request with all changes for review

**Key Design Principle:** The scanner does NOT use any hardcoded CVE databases or vulnerability patterns. All vulnerability information comes directly from GitHub Dependabot API. This ensures:
- Always up-to-date vulnerability data from GitHub's security advisory database
- No maintenance of hardcoded patterns required
- Consistent with GitHub's security recommendations
- Reliable detection based on actual security advisories

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
1. ✅ Scanner properly integrates with Dependabot API
2. ✅ Scanner does NOT use hardcoded vulnerability patterns
3. ✅ Scanner relies entirely on Dependabot for detection
4. ✅ Scanner provides clear error messages when Dependabot unavailable
5. ✅ Scanner correctly handles secure dependencies

The test suite automatically:
- Creates a backup of build.gradle
- Introduces a known vulnerable dependency (H2 2.1.214)
- Runs the scanner to verify it requires Dependabot API
- Verifies scanner doesn't use hardcoded patterns
- Tests the no-vulnerability case
- Restores the original state

**Note:** The tests verify that the scanner correctly requires Dependabot API access and does not fall back to hardcoded vulnerability detection. In environments without Dependabot API access, the scanner will report an error rather than using unreliable hardcoded patterns.

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
