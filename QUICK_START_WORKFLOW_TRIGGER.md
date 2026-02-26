# Quick Reference: Triggering Workflows on copilot/add-dependency-vulnerability

## Problem
Branch `copilot/add-dependency-vulnerability` is not showing in the GitHub UI dropdown when trying to manually trigger workflows.

## Quick Solutions

### Option 1: GitHub CLI (Recommended - Easiest)

```bash
# Install GitHub CLI if needed
# macOS: brew install gh
# Linux: See https://cli.github.com/
# Windows: scoop install gh

# Authenticate
gh auth login

# Run the interactive script
cd /path/to/Springboot-demo
./scripts/trigger-workflow.sh copilot/add-dependency-vulnerability
```

### Option 2: Python API Script (No GitHub CLI needed)

```bash
# Install requests library
pip install requests

# Set your GitHub token
export GITHUB_TOKEN=your_personal_access_token

# Trigger CVE Scanner workflow
python scripts/trigger_workflow_api.py \
  --workflow cve-scanner.yml \
  --branch copilot/add-dependency-vulnerability

# Trigger CodeQL workflow
python scripts/trigger_workflow_api.py \
  --workflow codeql.yml \
  --branch copilot/add-dependency-vulnerability

# Trigger SonarCloud workflow
python scripts/trigger_workflow_api.py \
  --workflow sonarcloud.yml \
  --branch copilot/add-dependency-vulnerability

# Trigger all at once
python scripts/trigger_workflow_api.py \
  --workflow cve-scanner.yml \
  --workflow codeql.yml \
  --workflow sonarcloud.yml \
  --branch copilot/add-dependency-vulnerability
```

### Option 3: GitHub CLI One-liner

```bash
# Authenticate first
gh auth login

# Trigger specific workflow
gh workflow run cve-scanner.yml --ref copilot/add-dependency-vulnerability
gh workflow run codeql.yml --ref copilot/add-dependency-vulnerability
gh workflow run sonarcloud.yml --ref copilot/add-dependency-vulnerability

# Watch the run
gh run list --workflow=cve-scanner.yml --limit 5
gh run watch <run-id>
```

### Option 4: cURL (Direct API call)

```bash
# Get your token from: https://github.com/settings/tokens
# Required scopes: repo, workflow

GITHUB_TOKEN="your_token_here"
REPO="HCL1111/Springboot-demo"
WORKFLOW="cve-scanner.yml"
BRANCH="copilot/add-dependency-vulnerability"

curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW/dispatches" \
  -d "{\"ref\":\"$BRANCH\"}"
```

## Verification

After triggering, verify the workflow started:

```bash
# Using GitHub CLI
gh run list --workflow=cve-scanner.yml --limit 3

# Or visit the Actions page
open "https://github.com/HCL1111/Springboot-demo/actions"
```

## Creating a GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Workflow Trigger Token"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. Copy the token immediately (you won't see it again!)
7. Store it securely or add to your environment:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

## Why This Happens

GitHub Actions UI only shows branches in the dropdown if:
1. The workflow file exists on that branch ✅ (It does)
2. The workflow has `workflow_dispatch` enabled ✅ (It does)
3. GitHub has indexed the branch (May take time ⏰)

## Additional Help

- **Full Documentation**: See `WORKFLOW_BRANCH_AVAILABILITY.md`
- **Script Documentation**: See `scripts/README.md`
- **Diagnostic Workflow**: Run "List Workflow Branches" from GitHub Actions UI
- **GitHub Status**: Check https://www.githubstatus.com/ for any service issues

## Support

If you continue to have issues:
1. Wait 5-10 minutes and refresh the page
2. Clear browser cache
3. Try the GitHub CLI or API methods above
4. Check GitHub Actions status page
5. Contact GitHub Support if the issue persists beyond 24 hours
