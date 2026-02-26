# Workflow Branch Availability Guide

## Issue: Branch Not Available in Workflow Dropdown

### Problem Statement
When trying to manually trigger a GitHub Actions workflow using `workflow_dispatch`, the branch `copilot/add-dependency-vulnerability` (or other branches) may not appear in the branch selection dropdown.

### Root Cause Analysis

GitHub Actions requires the following conditions for a branch to appear in the manual trigger dropdown:

1. ✅ **The branch must exist** - The branch `copilot/add-dependency-vulnerability` exists in the repository
2. ✅ **The workflow file must exist on that branch** - All workflow files (cve-scanner.yml, codeql.yml, sonarcloud.yml) exist on the branch
3. ✅ **The workflow must have `workflow_dispatch` trigger** - The workflows have `workflow_dispatch` configured
4. ⚠️ **GitHub must have indexed the branch** - This can take time for newly created or updated branches

### Verification

Run the following commands to verify the branch and workflow files:

```bash
# Check if the branch exists remotely
git ls-remote --heads origin | grep copilot/add-dependency-vulnerability

# Fetch the branch
git fetch origin copilot/add-dependency-vulnerability

# Check workflow files on the branch
git ls-tree -r --name-only <commit-sha> -- .github/workflows/

# Verify workflow_dispatch is configured
git show <commit-sha>:.github/workflows/cve-scanner.yml | grep -A2 workflow_dispatch
```

### Solutions

#### Solution 1: Wait for GitHub to Index (Recommended)
GitHub Actions may need time to index newly created or updated branches. This typically takes a few minutes to a few hours.

**What to do:**
- Wait 5-10 minutes and refresh the GitHub Actions page
- Clear your browser cache if needed
- Try accessing the workflow from a different browser or incognito mode

#### Solution 2: Push a Small Change to the Branch
Sometimes triggering a new commit on the branch helps GitHub re-index it.

```bash
# Checkout the branch
git fetch origin copilot/add-dependency-vulnerability:copilot/add-dependency-vulnerability
git checkout copilot/add-dependency-vulnerability

# Make a trivial change (e.g., update a comment in a workflow)
# Push the change
git push origin copilot/add-dependency-vulnerability
```

#### Solution 3: Trigger Workflow via GitHub CLI
You can trigger the workflow programmatically without using the UI:

```bash
# Install GitHub CLI if not already installed
# brew install gh  # macOS
# Or download from https://cli.github.com/

# Authenticate
gh auth login

# Trigger the workflow on the specific branch
gh workflow run "CVE Scanner and Auto-Fix" --ref copilot/add-dependency-vulnerability
gh workflow run "CodeQL Advanced" --ref copilot/add-dependency-vulnerability
gh workflow run "SonarCloud Analysis" --ref copilot/add-dependency-vulnerability
```

#### Solution 4: Trigger Workflow via API
Use the GitHub API to trigger the workflow:

```bash
# Get your GitHub token (Settings > Developer settings > Personal access tokens)
# Replace <TOKEN>, <WORKFLOW_ID>, and <BRANCH> with actual values

curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token <TOKEN>" \
  https://api.github.com/repos/HCL1111/Springboot-demo/actions/workflows/<WORKFLOW_ID>/dispatches \
  -d '{"ref":"copilot/add-dependency-vulnerability"}'
```

Workflow IDs:
- CVE Scanner: `cve-scanner.yml`
- CodeQL: `codeql.yml`
- SonarCloud: `sonarcloud.yml`

### Known GitHub Issues
- GitHub Actions UI caching can cause branches not to appear immediately
- Branches with special characters or very long names may have display issues
- Workflow files must be valid YAML or the branch won't appear

### Current Status

✅ **Verified on `copilot/add-dependency-vulnerability` branch:**
- Branch exists remotely: ✓
- Workflow files present: ✓
  - `.github/workflows/cve-scanner.yml` ✓
  - `.github/workflows/codeql.yml` ✓
  - `.github/workflows/sonarcloud.yml` ✓
  - `.github/workflows/dependency-submission.yml` ✓
- `workflow_dispatch` configured: ✓

**The branch meets all requirements and should be available for manual workflow triggers.**

### Recommendations

1. **Try the GitHub CLI approach** (Solution 3) - Most reliable method
2. **Wait and refresh** - Often resolves itself within minutes
3. **Check GitHub Status** - Visit https://www.githubstatus.com/ to ensure there are no ongoing incidents
4. **Contact GitHub Support** - If the issue persists beyond 24 hours

### Testing the Fix

After applying any solution, verify the workflow can be triggered:

1. Go to: https://github.com/HCL1111/Springboot-demo/actions
2. Select a workflow (e.g., "CVE Scanner and Auto-Fix")
3. Click "Run workflow" button
4. Check if `copilot/add-dependency-vulnerability` appears in the branch dropdown
5. Select the branch and click "Run workflow"

### Additional Resources

- [GitHub Actions: Manual workflow triggers](https://docs.github.com/en/actions/managing-workflow-runs/manually-running-a-workflow)
- [GitHub Actions: workflow_dispatch event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch)
- [GitHub CLI: workflow command](https://cli.github.com/manual/gh_workflow_run)
