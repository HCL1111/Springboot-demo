#!/usr/bin/env python3
"""
GitHub Workflow Trigger Script (API-based)

This script triggers GitHub Actions workflows on specific branches using the GitHub API.
Use this when branches don't appear in the GitHub UI dropdown for manual workflow triggers.

Requirements:
    pip install requests

Usage:
    python scripts/trigger_workflow_api.py --workflow cve-scanner.yml --branch copilot/add-dependency-vulnerability
    
    # Or set GITHUB_TOKEN environment variable
    export GITHUB_TOKEN=your_token_here
    python scripts/trigger_workflow_api.py --workflow cve-scanner.yml --branch copilot/add-dependency-vulnerability
"""

import argparse
import os
import sys
import requests
from typing import List, Dict, Optional


class GitHubWorkflowTrigger:
    """Helper class to trigger GitHub Actions workflows via API."""
    
    def __init__(self, repo: str, token: Optional[str] = None):
        self.repo = repo
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.base_url = f"https://api.github.com/repos/{repo}"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}' if self.token else None
        }
    
    def verify_branch_exists(self, branch: str) -> bool:
        """Check if a branch exists in the repository."""
        url = f"{self.base_url}/branches/{branch}"
        response = requests.get(url, headers=self.headers)
        return response.status_code == 200
    
    def list_workflows(self) -> List[Dict]:
        """List all workflows in the repository."""
        url = f"{self.base_url}/actions/workflows"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('workflows', [])
    
    def get_workflow_id(self, workflow_name: str) -> Optional[int]:
        """Get workflow ID by name or path."""
        workflows = self.list_workflows()
        
        for workflow in workflows:
            if workflow['path'] == f".github/workflows/{workflow_name}" or workflow['name'] == workflow_name:
                return workflow['id']
        
        return None
    
    def trigger_workflow(self, workflow: str, branch: str, inputs: Optional[Dict] = None) -> bool:
        """
        Trigger a workflow on a specific branch.
        
        Args:
            workflow: Workflow filename (e.g., 'cve-scanner.yml') or workflow ID
            branch: Branch name to run the workflow on
            inputs: Optional inputs for the workflow
            
        Returns:
            True if successful, False otherwise
        """
        # Get workflow ID if workflow name was provided
        if isinstance(workflow, str) and not workflow.isdigit():
            workflow_id = self.get_workflow_id(workflow)
            if not workflow_id:
                print(f"❌ Workflow '{workflow}' not found")
                return False
        else:
            workflow_id = workflow
        
        url = f"{self.base_url}/actions/workflows/{workflow_id}/dispatches"
        
        payload = {
            'ref': branch
        }
        
        if inputs:
            payload['inputs'] = inputs
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 204:
            return True
        else:
            print(f"❌ Failed to trigger workflow: {response.status_code}")
            print(f"Response: {response.text}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Trigger GitHub Actions workflows on specific branches',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Trigger CVE scanner on a specific branch
    python trigger_workflow_api.py --workflow cve-scanner.yml --branch copilot/add-dependency-vulnerability
    
    # Trigger multiple workflows
    python trigger_workflow_api.py --workflow cve-scanner.yml --workflow codeql.yml --branch my-branch
    
    # Use custom repository
    python trigger_workflow_api.py --repo owner/repo --workflow my-workflow.yml --branch main
        """
    )
    
    parser.add_argument(
        '--repo',
        default='HCL1111/Springboot-demo',
        help='Repository in format owner/repo (default: HCL1111/Springboot-demo)'
    )
    
    parser.add_argument(
        '--workflow',
        action='append',
        required=True,
        help='Workflow filename (e.g., cve-scanner.yml). Can be specified multiple times.'
    )
    
    parser.add_argument(
        '--branch',
        required=True,
        help='Branch to run the workflow on'
    )
    
    parser.add_argument(
        '--token',
        help='GitHub personal access token (or set GITHUB_TOKEN env var)'
    )
    
    parser.add_argument(
        '--list-workflows',
        action='store_true',
        help='List all workflows and exit'
    )
    
    args = parser.parse_args()
    
    # Initialize trigger helper
    trigger = GitHubWorkflowTrigger(args.repo, args.token)
    
    if not trigger.token:
        print("❌ GitHub token not provided. Set GITHUB_TOKEN environment variable or use --token")
        sys.exit(1)
    
    # List workflows if requested
    if args.list_workflows:
        print(f"Workflows in {args.repo}:")
        print("-" * 80)
        workflows = trigger.list_workflows()
        for wf in workflows:
            print(f"  Name: {wf['name']}")
            print(f"  Path: {wf['path']}")
            print(f"  ID: {wf['id']}")
            print()
        sys.exit(0)
    
    # Verify branch exists
    print(f"Verifying branch '{args.branch}' exists...")
    if not trigger.verify_branch_exists(args.branch):
        print(f"❌ Branch '{args.branch}' not found in {args.repo}")
        sys.exit(1)
    
    print(f"✅ Branch '{args.branch}' exists")
    print()
    
    # Trigger workflows
    print("=" * 80)
    print("Triggering Workflows")
    print("=" * 80)
    
    success_count = 0
    fail_count = 0
    
    for workflow in args.workflow:
        print(f"\nTriggering: {workflow} on branch: {args.branch}")
        
        if trigger.trigger_workflow(workflow, args.branch):
            print(f"✅ Successfully triggered {workflow}")
            success_count += 1
        else:
            print(f"❌ Failed to trigger {workflow}")
            fail_count += 1
    
    # Summary
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print()
    print(f"View workflow runs: https://github.com/{args.repo}/actions")
    
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == '__main__':
    main()
