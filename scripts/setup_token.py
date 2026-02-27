#!/usr/bin/env python3
"""
GitHub Token Setup and Validation Tool

This tool helps users set up their GitHub Personal Access Token
with the correct permissions to use the CVE scanner.
"""

import os
import sys
import requests
import json
from typing import Dict, List, Tuple


class TokenValidator:
    """Validates GitHub token and provides setup guidance"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.repo = os.getenv("GITHUB_REPOSITORY", "")
        self.issues: List[str] = []
        self.warnings: List[str] = []
        
    def run(self) -> bool:
        """Run full validation and provide guidance"""
        print("=" * 80)
        print("GitHub Token Validator for CVE Scanner")
        print("=" * 80)
        print()
        
        # Check if token exists
        if not self.token:
            self.print_token_setup_guide()
            return False
        
        # Check if repository is set
        if not self.repo:
            print("⚠️  GITHUB_REPOSITORY not set")
            print("   For personal use, set it to: owner/repo")
            print("   Example: export GITHUB_REPOSITORY=HCL1111/Springboot-demo")
            print()
            repo_input = input("Enter repository (owner/repo) or press Enter to skip: ").strip()
            if repo_input and "/" in repo_input:
                self.repo = repo_input
                print(f"✅ Using repository: {self.repo}")
            else:
                print("❌ Cannot proceed without repository")
                return False
        
        print(f"🔍 Validating token for repository: {self.repo}")
        print()
        
        # Run validation tests
        token_valid = self.validate_token()
        repo_accessible = self.validate_repo_access()
        dependabot_enabled = self.check_dependabot_enabled()
        dependabot_accessible = self.test_dependabot_api()
        
        # Print summary
        print()
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        if token_valid and repo_accessible and dependabot_accessible:
            print("✅ All checks passed! Your token is configured correctly.")
            print()
            print("You can now run the CVE scanner:")
            print("   python scripts/fix_cves.py")
            return True
        else:
            print("❌ Some checks failed. Please review the issues below:")
            print()
            
            if self.issues:
                print("ISSUES TO FIX:")
                for i, issue in enumerate(self.issues, 1):
                    print(f"  {i}. {issue}")
                print()
            
            if self.warnings:
                print("WARNINGS:")
                for warning in self.warnings:
                    print(f"  ⚠️  {warning}")
                print()
            
            # Provide specific guidance
            if not token_valid:
                self.print_token_setup_guide()
            elif not dependabot_accessible:
                self.print_dependabot_setup_guide()
            
            return False
    
    def validate_token(self) -> bool:
        """Validate token is working and has correct scopes"""
        print("1️⃣  Validating GitHub token...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        try:
            resp = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                user_data = resp.json()
                username = user_data.get('login', 'Unknown')
                print(f"   ✅ Token valid - Authenticated as: {username}")
                
                # Check scopes
                scopes = resp.headers.get('X-OAuth-Scopes', '')
                if scopes:
                    scopes_list = [s.strip() for s in scopes.split(',')]
                    print(f"   Token scopes: {', '.join(scopes_list)}")
                    
                    # Check for required scopes
                    has_repo = 'repo' in scopes_list or 'public_repo' in scopes_list
                    has_security = 'security_events' in scopes_list
                    
                    if not has_repo:
                        self.warnings.append("Token missing 'repo' scope - may have limited access")
                    
                    if not has_security:
                        self.issues.append("Token missing 'security_events' scope - REQUIRED for Dependabot API")
                        print(f"   ❌ Missing required scope: security_events")
                        return False
                    else:
                        print(f"   ✅ Has security_events scope")
                else:
                    # Fine-grained token - different permission model
                    print(f"   ℹ️  Fine-grained token detected")
                    self.warnings.append("Fine-grained token - ensure 'Security events' permission is set to Read-only")
                
                return True
            elif resp.status_code == 401:
                print(f"   ❌ Token invalid or expired")
                self.issues.append("Token is invalid or expired")
                return False
            elif resp.status_code == 403:
                print(f"   ❌ Access forbidden")
                error_msg = resp.json().get('message', resp.text[:200])
                print(f"   Error: {error_msg}")
                self.issues.append(f"API access forbidden: {error_msg}")
                return False
            else:
                print(f"   ❌ Unexpected status: {resp.status_code}")
                self.issues.append(f"Unexpected API response: {resp.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Cannot connect to GitHub API")
            print(f"   Check your internet connection")
            self.issues.append("Cannot connect to GitHub API - check internet connection")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.issues.append(f"Error validating token: {e}")
            return False
    
    def validate_repo_access(self) -> bool:
        """Validate access to the repository"""
        print()
        print("2️⃣  Validating repository access...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        try:
            url = f"https://api.github.com/repos/{self.repo}"
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                repo_data = resp.json()
                print(f"   ✅ Repository accessible: {repo_data.get('full_name')}")
                print(f"   Private: {repo_data.get('private', False)}")
                
                permissions = repo_data.get('permissions', {})
                if permissions:
                    print(f"   Permissions: admin={permissions.get('admin')}, push={permissions.get('push')}, pull={permissions.get('pull')}")
                
                return True
            elif resp.status_code == 404:
                print(f"   ❌ Repository not found")
                self.issues.append(f"Repository '{self.repo}' not found or not accessible")
                return False
            elif resp.status_code == 403:
                print(f"   ❌ Access forbidden")
                self.issues.append(f"No permission to access repository '{self.repo}'")
                return False
            else:
                print(f"   ❌ Unexpected status: {resp.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def check_dependabot_enabled(self) -> bool:
        """Check if Dependabot is enabled on the repository"""
        print()
        print("3️⃣  Checking if Dependabot is enabled...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        try:
            url = f"https://api.github.com/repos/{self.repo}/vulnerability-alerts"
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 204:
                print(f"   ✅ Dependabot vulnerability alerts are ENABLED")
                return True
            elif resp.status_code == 404:
                print(f"   ⚠️  Dependabot vulnerability alerts are DISABLED")
                self.warnings.append("Dependabot is not enabled - enable it in repository settings")
                print(f"   Enable at: https://github.com/{self.repo}/settings/security_analysis")
                return False
            else:
                print(f"   ⚠️  Cannot determine Dependabot status (status: {resp.status_code})")
                return False
                
        except Exception as e:
            print(f"   ⚠️  Error checking Dependabot status: {e}")
            return False
    
    def test_dependabot_api(self) -> bool:
        """Test access to Dependabot alerts API"""
        print()
        print("4️⃣  Testing Dependabot alerts API access...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        try:
            url = f"https://api.github.com/repos/{self.repo}/dependabot/alerts"
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                alerts = resp.json()
                print(f"   ✅ Dependabot API accessible")
                print(f"   Found {len(alerts)} Dependabot alert(s)")
                
                # Show summary of alerts
                if alerts:
                    open_alerts = [a for a in alerts if a.get('state') == 'open']
                    print(f"   Open alerts: {len(open_alerts)}")
                
                return True
            elif resp.status_code == 403:
                print(f"   ❌ Access forbidden to Dependabot API")
                error_data = resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('message', resp.text[:200])
                print(f"   Error: {error_msg}")
                
                if 'security_events' in error_msg.lower() or 'permission' in error_msg.lower():
                    self.issues.append("Token lacks 'security_events' permission for Dependabot API")
                else:
                    self.issues.append(f"Dependabot API access denied: {error_msg}")
                
                return False
            elif resp.status_code == 404:
                print(f"   ⚠️  Dependabot alerts not available")
                self.warnings.append("Dependabot alerts may not be enabled for this repository")
                return False
            else:
                print(f"   ❌ Unexpected status: {resp.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def print_token_setup_guide(self):
        """Print detailed token setup guide"""
        print()
        print("=" * 80)
        print("HOW TO CREATE A GITHUB PERSONAL ACCESS TOKEN")
        print("=" * 80)
        print()
        print("For the CVE scanner to work with your personal GitHub account,")
        print("you need to create a Personal Access Token with the right permissions.")
        print()
        print("📋 STEP-BY-STEP GUIDE:")
        print()
        print("1. Go to GitHub Settings:")
        print("   https://github.com/settings/tokens")
        print()
        print("2. Choose token type:")
        print()
        print("   Option A - Classic Token (Recommended for simplicity):")
        print("   ─────────────────────────────────────────────────────")
        print("   • Click 'Generate new token' → 'Generate new token (classic)'")
        print("   • Give it a name: 'CVE Scanner'")
        print("   • Select scopes:")
        print("     ✓ repo (Full control of private repositories)")
        print("     ✓ security_events (Read and write security events) ⭐ REQUIRED")
        print("   • Click 'Generate token'")
        print()
        print("   Option B - Fine-grained Token (More secure, limited scope):")
        print("   ───────────────────────────────────────────────────────────")
        print("   • Click 'Generate new token' → 'Generate new token (beta)'")
        print("   • Repository access: Select 'Only select repositories'")
        print("   • Choose your repository (e.g., HCL1111/Springboot-demo)")
        print("   • Permissions:")
        print("     - Contents: Read and write")
        print("     - Metadata: Read-only (auto-selected)")
        print("     - Pull requests: Read and write")
        print("     - Security events: Read-only ⭐ REQUIRED")
        print("   • Click 'Generate token'")
        print()
        print("3. Copy the token (it won't be shown again!)")
        print()
        print("4. Set environment variables:")
        print()
        print("   On Linux/Mac:")
        print("   ──────────────")
        print("   export GITHUB_TOKEN='your_token_here'")
        print(f"   export GITHUB_REPOSITORY='{self.repo or 'owner/repo'}'")
        print()
        print("   On Windows (PowerShell):")
        print("   ────────────────────────")
        print("   $env:GITHUB_TOKEN='your_token_here'")
        print(f"   $env:GITHUB_REPOSITORY='{self.repo or 'owner/repo'}'")
        print()
        print("   On Windows (CMD):")
        print("   ─────────────────")
        print("   set GITHUB_TOKEN=your_token_here")
        print(f"   set GITHUB_REPOSITORY={self.repo or 'owner/repo'}")
        print()
        print("5. Run this validator again to verify:")
        print("   python scripts/setup_token.py")
        print()
        print("=" * 80)
    
    def print_dependabot_setup_guide(self):
        """Print guide for enabling Dependabot"""
        print()
        print("=" * 80)
        print("HOW TO ENABLE DEPENDABOT")
        print("=" * 80)
        print()
        print(f"1. Go to: https://github.com/{self.repo}/settings/security_analysis")
        print()
        print("2. Enable:")
        print("   ✓ Dependabot alerts")
        print("   ✓ Dependabot security updates (optional but recommended)")
        print()
        print("3. Wait a few minutes for GitHub to scan your dependencies")
        print()
        print("4. Run this validator again:")
        print("   python scripts/setup_token.py")
        print()
        print("=" * 80)


def main():
    """Main entry point"""
    validator = TokenValidator()
    success = validator.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
