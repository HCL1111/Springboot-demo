#!/bin/bash

# Script to trigger GitHub Actions workflows on specific branches
# This is a workaround when branches don't appear in the GitHub UI dropdown

set -e

# Configuration
REPO="HCL1111/Springboot-demo"
BRANCH="${1:-copilot/add-dependency-vulnerability}"

echo "========================================="
echo "GitHub Workflow Trigger Script"
echo "========================================="
echo "Repository: $REPO"
echo "Target Branch: $BRANCH"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo ""
    echo "To install:"
    echo "  macOS:   brew install gh"
    echo "  Linux:   See https://github.com/cli/cli#installation"
    echo "  Windows: scoop install gh"
    echo ""
    echo "Or use the GitHub API method instead (see WORKFLOW_BRANCH_AVAILABILITY.md)"
    exit 1
fi

echo "✅ GitHub CLI found"
echo ""

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub"
    echo "Run: gh auth login"
    exit 1
fi

echo "✅ GitHub authentication verified"
echo ""

# Verify the branch exists
echo "Verifying branch exists..."
if ! gh api "repos/$REPO/branches/$BRANCH" &> /dev/null; then
    echo "❌ Branch '$BRANCH' not found in repository"
    echo ""
    echo "Available branches:"
    gh api "repos/$REPO/branches" --jq '.[].name' | head -10
    exit 1
fi

echo "✅ Branch '$BRANCH' exists"
echo ""

# List available workflows
echo "Available workflows:"
gh workflow list --repo "$REPO"
echo ""

# Prompt user to select workflow or trigger all
echo "Which workflow would you like to trigger?"
echo "1) CVE Scanner and Auto-Fix (cve-scanner.yml)"
echo "2) CodeQL Advanced (codeql.yml)"
echo "3) SonarCloud Analysis (sonarcloud.yml)"
echo "4) All workflows with workflow_dispatch"
echo "5) Custom workflow name"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        WORKFLOWS=("cve-scanner.yml")
        ;;
    2)
        WORKFLOWS=("codeql.yml")
        ;;
    3)
        WORKFLOWS=("sonarcloud.yml")
        ;;
    4)
        WORKFLOWS=("cve-scanner.yml" "codeql.yml" "sonarcloud.yml")
        ;;
    5)
        read -p "Enter workflow file name (e.g., my-workflow.yml): " custom_workflow
        WORKFLOWS=("$custom_workflow")
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Triggering Workflows"
echo "========================================="

for workflow in "${WORKFLOWS[@]}"; do
    echo ""
    echo "Triggering: $workflow on branch: $BRANCH"
    
    if gh workflow run "$workflow" --repo "$REPO" --ref "$BRANCH"; then
        echo "✅ Successfully triggered $workflow"
        
        # Show recent runs
        echo ""
        echo "Recent runs:"
        gh run list --workflow="$workflow" --repo "$REPO" --limit 3
    else
        echo "❌ Failed to trigger $workflow"
        echo "   This workflow may not have workflow_dispatch enabled on this branch"
    fi
done

echo ""
echo "========================================="
echo "Complete!"
echo "========================================="
echo ""
echo "To view workflow runs:"
echo "  gh run list --repo $REPO"
echo ""
echo "To watch a specific run:"
echo "  gh run watch <run-id> --repo $REPO"
echo ""
echo "Or visit: https://github.com/$REPO/actions"
