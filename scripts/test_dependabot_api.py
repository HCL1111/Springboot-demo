#!/usr/bin/env python3
"""
Simple test script to verify Dependabot API access with a token.

This script tests if a GitHub token has the correct permissions
to access the Dependabot alerts API.

Usage:
    export GITHUB_TOKEN='your_token_here'
    export GITHUB_REPOSITORY='owner/repo'
    python scripts/test_dependabot_api.py
"""

import os
import sys
import requests
import json
from datetime import datetime


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def test_dependabot_api():
    """Test Dependabot API access"""
    
    # Get environment variables
    token = os.getenv("GITHUB_TOKEN", "")
    repo = os.getenv("GITHUB_REPOSITORY", "")
    
    print_header("Dependabot API Test")
    print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repository: {repo}")
    print(f"Token: {token[:10]}..." if len(token) > 10 else "Token: [NOT SET]")
    print()
    
    if not token:
        print("❌ ERROR: GITHUB_TOKEN environment variable is not set")
        print("\nPlease set it:")
        print("  export GITHUB_TOKEN='your_token_here'")
        return False
    
    if not repo:
        print("❌ ERROR: GITHUB_REPOSITORY environment variable is not set")
        print("\nPlease set it:")
        print("  export GITHUB_REPOSITORY='owner/repo'")
        return False
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # Test 1: Validate token with /user endpoint
    print_header("Test 1: Validate Token")
    print("Testing endpoint: GET https://api.github.com/user")
    
    try:
        resp = requests.get("https://api.github.com/user", headers=headers, timeout=10)
        
        if resp.status_code == 200:
            user_data = resp.json()
            username = user_data.get('login', 'Unknown')
            print(f"✅ SUCCESS - Authenticated as: {username}")
            
            # Check scopes
            scopes = resp.headers.get('X-OAuth-Scopes', '')
            if scopes:
                scopes_list = [s.strip() for s in scopes.split(',')]
                print(f"✅ Token scopes: {', '.join(scopes_list)}")
                
                # Check for required scopes
                has_security = 'security_events' in scopes_list
                if has_security:
                    print(f"✅ Has 'security_events' scope - REQUIRED for Dependabot API")
                else:
                    print(f"❌ Missing 'security_events' scope - REQUIRED for Dependabot API")
                    print(f"\nThe token will NOT work with Dependabot API without this scope.")
                    print(f"Please create a new token with 'security_events' scope.")
                    return False
            else:
                print(f"ℹ️  Fine-grained token detected")
                print(f"   Make sure 'Security events' permission is set to 'Read-only'")
        elif resp.status_code == 401:
            print(f"❌ FAILED - Token is invalid or expired")
            print(f"   HTTP Status: {resp.status_code}")
            return False
        elif resp.status_code == 403:
            print(f"❌ FAILED - Access forbidden")
            print(f"   HTTP Status: {resp.status_code}")
            error_msg = resp.text[:200]
            print(f"   Error: {error_msg}")
            
            # Check if it's due to DNS proxy (common in CI environments)
            if "DNS monitoring proxy" in error_msg or "Blocked by" in error_msg:
                print(f"\n⚠️  NOTE: This appears to be a network/proxy block, not a token issue.")
                print(f"   The token may work fine on your local machine.")
                print(f"   This is expected in GitHub Actions environments.")
            
            return False
        else:
            print(f"❌ FAILED - Unexpected status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED - Network error: {e}")
        print(f"\n⚠️  This may be due to network restrictions in CI environment.")
        return False
    
    # Test 2: Check repository access
    print_header("Test 2: Repository Access")
    print(f"Testing endpoint: GET https://api.github.com/repos/{repo}")
    
    try:
        resp = requests.get(f"https://api.github.com/repos/{repo}", headers=headers, timeout=10)
        
        if resp.status_code == 200:
            repo_data = resp.json()
            print(f"✅ SUCCESS - Repository accessible: {repo}")
            print(f"   Private: {repo_data.get('private', False)}")
            
            # Check permissions
            permissions = repo_data.get('permissions', {})
            print(f"   Permissions:")
            print(f"     - Admin: {permissions.get('admin', False)}")
            print(f"     - Push: {permissions.get('push', False)}")
            print(f"     - Pull: {permissions.get('pull', False)}")
        elif resp.status_code == 404:
            print(f"❌ FAILED - Repository not found or no access")
            print(f"   Make sure the token has access to: {repo}")
            return False
        elif resp.status_code == 403:
            print(f"❌ FAILED - Access forbidden")
            error_msg = resp.text[:200]
            print(f"   Error: {error_msg}")
            return False
        else:
            print(f"❌ FAILED - Unexpected status: {resp.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED - Network error: {e}")
        return False
    
    # Test 3: Check Dependabot enablement
    print_header("Test 3: Dependabot Enablement")
    print(f"Testing endpoint: GET https://api.github.com/repos/{repo}/vulnerability-alerts")
    
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{repo}/vulnerability-alerts",
            headers=headers,
            timeout=10
        )
        
        if resp.status_code == 204:
            print(f"✅ SUCCESS - Dependabot vulnerability alerts are ENABLED")
        elif resp.status_code == 404:
            print(f"⚠️  WARNING - Dependabot vulnerability alerts are DISABLED")
            print(f"   Enable at: https://github.com/{repo}/settings/security_analysis")
        else:
            print(f"⚠️  Cannot determine Dependabot status (status: {resp.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error checking Dependabot status: {e}")
    
    # Test 4: Test Dependabot API
    print_header("Test 4: Dependabot Alerts API ⭐ MAIN TEST")
    print(f"Testing endpoint: GET https://api.github.com/repos/{repo}/dependabot/alerts")
    
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{repo}/dependabot/alerts",
            headers=headers,
            timeout=10
        )
        
        if resp.status_code == 200:
            alerts = resp.json()
            print(f"✅ SUCCESS - Dependabot API is accessible!")
            print(f"✅ Found {len(alerts)} Dependabot alert(s)")
            
            if alerts:
                open_alerts = [a for a in alerts if a.get('state') == 'open']
                fixed_alerts = [a for a in alerts if a.get('state') == 'fixed']
                dismissed_alerts = [a for a in alerts if a.get('state') == 'dismissed']
                
                print(f"\nAlert Summary:")
                print(f"  - Open: {len(open_alerts)}")
                print(f"  - Fixed: {len(fixed_alerts)}")
                print(f"  - Dismissed: {len(dismissed_alerts)}")
                
                # Show details of open alerts
                if open_alerts:
                    print(f"\nOpen Alerts:")
                    for i, alert in enumerate(open_alerts[:5], 1):  # Show first 5
                        security_advisory = alert.get('security_advisory', {})
                        severity = security_advisory.get('severity', 'unknown')
                        cve_id = security_advisory.get('cve_id', 'N/A')
                        package = alert.get('dependency', {}).get('package', {}).get('name', 'Unknown')
                        
                        print(f"  {i}. {package}")
                        print(f"     CVE: {cve_id}")
                        print(f"     Severity: {severity.upper()}")
            else:
                print(f"\n🎉 No vulnerabilities found - repository is clean!")
            
            return True
            
        elif resp.status_code == 403:
            print(f"❌ FAILED - Access forbidden to Dependabot API")
            
            try:
                error_data = resp.json()
                error_msg = error_data.get('message', resp.text[:200])
            except:
                error_msg = resp.text[:200]
            
            print(f"   Error: {error_msg}")
            
            if 'security_events' in error_msg.lower():
                print(f"\n💡 SOLUTION:")
                print(f"   The token is missing the 'security_events' scope.")
                print(f"   Create a new token with this scope at:")
                print(f"   https://github.com/settings/tokens")
            elif "DNS monitoring proxy" in error_msg or "Blocked by" in error_msg:
                print(f"\n⚠️  NOTE: This is a network/proxy block, not a token issue.")
                print(f"   The token should work fine on your local machine.")
            
            return False
            
        elif resp.status_code == 404:
            print(f"⚠️  WARNING - Dependabot alerts not available")
            print(f"   Dependabot may not be enabled for this repository")
            print(f"   Enable at: https://github.com/{repo}/settings/security_analysis")
            return False
        else:
            print(f"❌ FAILED - Unexpected status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED - Network error: {e}")
        print(f"\n⚠️  This may be due to network restrictions in CI environment.")
        return False
    
    return True


def main():
    """Main entry point"""
    print("\n" + "🔒" * 40)
    print("GitHub Dependabot API Test")
    print("🔒" * 40)
    
    success = test_dependabot_api()
    
    print_header("FINAL RESULT")
    
    if success:
        print("✅ ALL TESTS PASSED")
        print("\nYour token is configured correctly and can access the Dependabot API!")
        print("You can now run the CVE scanner:")
        print("  python scripts/fix_cves.py")
        return 0
    else:
        print("❌ TESTS FAILED")
        print("\nThe token cannot access the Dependabot API.")
        print("\nPossible reasons:")
        print("  1. Missing 'security_events' scope")
        print("  2. Network/proxy blocking (if in CI environment)")
        print("  3. Token is invalid or expired")
        print("  4. Dependabot not enabled on repository")
        print("\nIf you're testing in GitHub Actions, this is expected.")
        print("The token should work on your local machine.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
