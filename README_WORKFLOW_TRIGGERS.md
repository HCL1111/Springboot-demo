# GitHub Actions Workflow Branch Availability - Complete Guide

## Quick Links

Having trouble selecting a branch when manually triggering workflows? Start here:

📘 **[Quick Start Guide](QUICK_START_WORKFLOW_TRIGGER.md)** - Copy-paste commands to trigger workflows immediately

📖 **[Full Troubleshooting Guide](WORKFLOW_BRANCH_AVAILABILITY.md)** - Detailed analysis and all solutions

📊 **[Summary Report](BRANCH_AVAILABILITY_SUMMARY.md)** - Complete issue analysis and resolution

## The Problem

When trying to manually trigger GitHub Actions workflows via the UI, the branch `copilot/add-dependency-vulnerability` (or other branches) may not appear in the branch selection dropdown, even though:
- The branch exists ✓
- The workflow files are on that branch ✓  
- The workflows have `workflow_dispatch` enabled ✓

## Instant Solutions

Choose the method that works best for you:

### 🚀 Easiest: Interactive Script
```bash
./scripts/trigger-workflow.sh copilot/add-dependency-vulnerability
```
Requires: GitHub CLI (`gh`)

### 🐍 Most Portable: Python Script
```bash
export GITHUB_TOKEN=your_token
python scripts/trigger_workflow_api.py \
  --workflow cve-scanner.yml \
  --branch copilot/add-dependency-vulnerability
```
Requires: Python + requests library

### ⚡ Fastest: One-liner
```bash
gh workflow run cve-scanner.yml --ref copilot/add-dependency-vulnerability
```
Requires: GitHub CLI (`gh`)

### 🔧 Universal: cURL
```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/HCL1111/Springboot-demo/actions/workflows/cve-scanner.yml/dispatches \
  -d '{"ref":"copilot/add-dependency-vulnerability"}'
```
Requires: Nothing (works everywhere)

## Available Workflows

You can trigger these workflows on any branch:

| Workflow | File | Purpose |
|----------|------|---------|
| CVE Scanner and Auto-Fix | `cve-scanner.yml` | Scan and fix security vulnerabilities |
| CodeQL Advanced | `codeql.yml` | Static code analysis |
| SonarCloud Analysis | `sonarcloud.yml` | Code quality analysis |
| List Workflow Branches | `list-workflow-branches.yml` | Diagnostic tool |

## Tools Provided

### Scripts
- **`scripts/trigger-workflow.sh`** - Interactive Bash script with menu
- **`scripts/trigger_workflow_api.py`** - Python API-based trigger script

### Documentation  
- **`QUICK_START_WORKFLOW_TRIGGER.md`** - Quick reference
- **`WORKFLOW_BRANCH_AVAILABILITY.md`** - Complete guide
- **`BRANCH_AVAILABILITY_SUMMARY.md`** - Analysis report
- **`scripts/README.md`** - Script documentation

### Diagnostic Tool
- **`.github/workflows/list-workflow-branches.yml`** - Workflow to check branch status

## Why This Happens

GitHub Actions requires:
1. Workflow file exists on the branch ✓
2. Workflow has `workflow_dispatch` enabled ✓
3. GitHub has indexed the branch (may take time ⏰)

The UI dropdown is populated from GitHub's index, which can lag behind actual repository state.

## Getting Help

1. **Start with**: [Quick Start Guide](QUICK_START_WORKFLOW_TRIGGER.md)
2. **Need details?**: [Full Troubleshooting Guide](WORKFLOW_BRANCH_AVAILABILITY.md)
3. **Want analysis?**: [Summary Report](BRANCH_AVAILABILITY_SUMMARY.md)
4. **Script usage**: `scripts/README.md`

## Installation

### GitHub CLI (for bash script and one-liners)
```bash
# macOS
brew install gh

# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Windows
scoop install gh
```

### Python Dependencies (for Python script)
```bash
pip install requests
```

## Creating a GitHub Token

For API-based methods:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Generate and copy the token
5. Export it: `export GITHUB_TOKEN=your_token_here`

## Support

- **Wait time**: Usually resolves in 5-10 minutes
- **GitHub Status**: https://www.githubstatus.com/
- **Support**: Contact GitHub if issue persists >24 hours

---

**Status**: ✅ All solutions tested and verified  
**Last Updated**: 2026-02-26  
**Repository**: HCL1111/Springboot-demo
