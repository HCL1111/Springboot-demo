#!/usr/bin/env python3
"""
Trigger the CVE Scanner workflow on GitHub.

This script triggers the existing GitHub Actions workflow that
will run the CVE scanner with proper permissions.

Usage:
    export GITHUB_TOKEN='your_token_here'
    python scripts/trigger_cve_workflow.py
"""

import os
import sys
import requests
import json
from datetime import datetime


def trigger_workflow():
    """Trigger the CVE Scanner workflow"""
    
    token = os.getenv("GITHUB_TOKEN", "")
    repo = os.getenv("GITHUB_REPOSITORY", "HCL1111/Springboot-demo")
    
    if not token:
        print("❌ ERROR: GITHUB_TOKEN environment variable is not set")
        print("\nSet it with:")
        print("  export GITHUB_TOKEN='your_token_here'")
        return False
    
    print("=" * 80)
    print("CVE Scanner Workflow Trigger")
    print("=" * 80)
    print()
    print(f"Repository: {repo}")
    print(f"Token: {token[:10]}...")
    print()
    
    # Prepare the API request
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # Workflow dispatch endpoint
    url = f"https://api.github.com/repos/{repo}/actions/workflows/cve-scanner.yml/dispatches"
    
    # Payload
    data = {
        "ref": "master",  # or the branch you want
        "inputs": {}
    }
    
    print("🚀 Triggering CVE Scanner workflow...")
    print(f"   Workflow: cve-scanner.yml")
    print(f"   Branch: master")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 204:
            print("✅ SUCCESS - Workflow triggered!")
            print()
            print("📋 Next steps:")
            print(f"   1. Go to: https://github.com/{repo}/actions")
            print(f"   2. Look for the running 'CVE Scanner and Auto-Fix' workflow")
            print(f"   3. Click on it to see the progress")
            print(f"   4. Wait for it to complete (~3-5 minutes)")
            print(f"   5. Check for the Pull Request it creates")
            print()
            print("The workflow will:")
            print("   • Scan for vulnerabilities using Dependabot API")
            print("   • Detect CVE-2024-47554 in commons-io:2.13.0")
            print("   • Update to commons-io:2.18.0")
            print("   • Run Gradle build to verify")
            print("   • Create a Pull Request with the fix")
            print()
            return True
        elif response.status_code == 403:
            print("❌ FAILED - Permission denied")
            print(f"   HTTP Status: {response.status_code}")
            print()
            error_msg = response.json().get("message", "") if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"   Error: {error_msg}")
            print()
            print("💡 Possible reasons:")
            print("   1. Token doesn't have 'workflow' scope")
            print("   2. Token doesn't have 'repo' scope")
            print("   3. Not repository admin/write access")
            print()
            print("🔧 To fix:")
            print("   1. Go to: https://github.com/settings/tokens")
            print("   2. Create token with scopes:")
            print("      • repo")
            print("      • workflow")
            print("      • security_events")
            return False
        elif response.status_code == 404:
            print("❌ FAILED - Workflow not found")
            print(f"   HTTP Status: {response.status_code}")
            print()
            print("   The workflow file may not exist or may have a different name.")
            print(f"   Check: https://github.com/{repo}/tree/master/.github/workflows")
            return False
        elif response.status_code == 422:
            print("❌ FAILED - Invalid request")
            print(f"   HTTP Status: {response.status_code}")
            print()
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            print(f"   Error: {error_data.get('message', 'Invalid workflow dispatch request')}")
            print()
            print("   Possible issues:")
            print("   • Branch 'master' doesn't exist (try 'main')")
            print("   • Workflow doesn't have workflow_dispatch trigger")
            return False
        else:
            print(f"❌ FAILED - Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED - Network error: {e}")
        print()
        print("   If you're seeing a DNS proxy error, you're in a restricted environment.")
        print("   Run this script on your personal laptop instead.")
        return False


def main():
    """Main entry point"""
    print()
    print("🔧" * 40)
    print("CVE Scanner Workflow Trigger")
    print("🔧" * 40)
    print()
    
    success = trigger_workflow()
    
    if success:
        print("=" * 80)
        print("✅ Workflow triggered successfully!")
        print("=" * 80)
        return 0
    else:
        print("=" * 80)
        print("❌ Failed to trigger workflow")
        print("=" * 80)
        print()
        print("Alternative: Trigger manually via web UI")
        print(f"1. Go to: https://github.com/HCL1111/Springboot-demo/actions/workflows/cve-scanner.yml")
        print(f"2. Click 'Run workflow' button")
        print(f"3. Select branch (master)")
        print(f"4. Click 'Run workflow'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
