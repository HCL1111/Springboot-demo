#!/usr/bin/env python3
"""
CVE Vulnerability Scanner and Fixer for Gradle Projects

This script:
1. Analyzes Gradle dependencies for known CVEs using GitHub Dependency Graph API
2. Automatically updates vulnerable dependencies to secure versions
3. Runs Gradle build and tests to verify fixes
4. Creates a PR with the changes using GitHub CLI
"""

import subprocess
import sys
import os
import re
import json
import time
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from datetime import datetime

# Try to import required packages, install if missing
try:
    import requests
except ImportError:
    print("Installing required package: requests")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


class CVEScanner:
    """Scanner for analyzing and fixing CVEs in Gradle dependencies"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.build_gradle = self.project_root / "build.gradle"
        self.vulnerabilities: List[Dict] = []
        self.fixes_applied: List[Dict] = []
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.repo_owner = os.getenv("GITHUB_REPOSITORY", "").split("/")[0] if os.getenv("GITHUB_REPOSITORY") else ""
        self.repo_name = os.getenv("GITHUB_REPOSITORY", "").split("/")[1] if os.getenv("GITHUB_REPOSITORY") else ""
        
    def run(self):
        """Main execution flow"""
        print("=" * 80)
        print("CVE Vulnerability Scanner and Fixer")
        print("=" * 80)
        print()
        
        # Step 1: Scan for vulnerabilities
        print("Step 1: Scanning for vulnerabilities...")
        self.scan_with_github_dependabot()
        
        # Step 2: Parse and analyze results
        print("\nStep 2: Analyzing vulnerabilities...")
        self.analyze_vulnerabilities()
        
        # Step 3: Apply fixes
        if self.vulnerabilities:
            print(f"\nStep 3: Found {len(self.vulnerabilities)} vulnerabilities. Applying fixes...")
            self.fix_vulnerabilities()
            
            # Step 4: Run Gradle build and tests
            print("\nStep 4: Running Gradle build and tests...")
            if not self.verify_build():
                print("ERROR: Build or tests failed after applying fixes!")
                return 1
            
            # Step 5: Generate summary report
            print("\nStep 5: Generating summary report...")
            self.generate_report()
            
            # Step 6: Create PR
            print("\nStep 6: Creating Pull Request...")
            self.create_pull_request()
        else:
            print("\n✅ No vulnerabilities found! All dependencies are secure.")
            return 0
        
        print("\n" + "=" * 80)
        print("✅ CVE fixes completed successfully!")
        print("=" * 80)
        return 0
    
    def scan_with_github_dependabot(self):
        """Scan using GitHub Dependabot alerts API"""
        print("Checking GitHub Dependabot alerts...")
        
        if not self.github_token or not self.repo_owner or not self.repo_name:
            print("⚠️  GitHub credentials not available, using manual scanning...")
            self.manual_cve_check()
            return
        
        try:
            # Get Dependabot alerts
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github+json"
            }
            
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/dependabot/alerts"
            
            # First, try to get all alerts (not just open ones)
            # This helps catch dismissed or auto-closed alerts that may still represent vulnerabilities
            response_all = requests.get(url, headers=headers)
            
            if response_all.status_code == 200:
                all_alerts = response_all.json()
                print(f"Found {len(all_alerts)} total Dependabot alerts (all states)")
                
                # Filter for alerts that represent current vulnerabilities
                # Include: open, dismissed (might be false dismissal), auto_dismissed
                # Exclude: fixed (truly resolved)
                for alert in all_alerts:
                    state = alert.get("state", "")
                    
                    # Skip truly fixed alerts
                    if state == "fixed":
                        continue
                    
                    vuln = alert.get("security_vulnerability", {})
                    package = vuln.get("package", {})
                    advisory = alert.get("security_advisory", {})
                    
                    # Check if the current dependency version is still vulnerable
                    # by comparing against our actual dependencies
                    dependencies = self.parse_gradle_dependencies()
                    package_name = package.get("name", "Unknown")
                    
                    # Check if this package is in our current dependencies
                    is_current = False
                    for dep in dependencies:
                        dep_name = f"{dep['group']}:{dep['artifact']}"
                        if dep_name == package_name or dep['artifact'] == package_name.split(':')[-1]:
                            is_current = True
                            break
                    
                    # Only add if it's a current dependency OR if it's an open alert
                    if is_current or state == "open":
                        self.vulnerabilities.append({
                            'package': package_name,
                            'ecosystem': package.get("ecosystem", "Unknown"),
                            'current_version': vuln.get("vulnerable_version_range", "Unknown"),
                            'patched_version': vuln.get("first_patched_version", {}).get("identifier", "Unknown"),
                            'cve': advisory.get("cve_id", advisory.get("ghsa_id", "Unknown")),
                            'severity': advisory.get("severity", "Unknown"),
                            'description': advisory.get("description", ""),
                            'cvss_score': advisory.get("cvss", {}).get("score", 0),
                            'alert_state': state
                        })
                
                print(f"Identified {len(self.vulnerabilities)} vulnerabilities affecting current dependencies")
                
                # If no vulnerabilities found via Dependabot, also run manual check
                if len(self.vulnerabilities) == 0:
                    print("No Dependabot vulnerabilities found, running manual check...")
                    self.manual_cve_check()
            else:
                print(f"⚠️  Could not fetch Dependabot alerts (status {response_all.status_code})")
                print("Falling back to manual scanning...")
                self.manual_cve_check()
                
        except Exception as e:
            print(f"⚠️  Error fetching Dependabot alerts: {e}")
            print("Falling back to manual scanning...")
            self.manual_cve_check()
    
    def manual_cve_check(self):
        """Manually check dependencies against known CVEs using Maven Central API"""
        print("Performing manual CVE check of current dependencies...")
        
        # Parse build.gradle to extract dependencies
        dependencies = self.parse_gradle_dependencies()
        
        print(f"Checking {len(dependencies)} dependencies against Maven Central...")
        
        for dep in dependencies:
            # Check if dependency has known vulnerabilities
            # Using a simple version check against known secure versions
            group_artifact = f"{dep['group']}:{dep['artifact']}"
            
            # Check against known patterns of vulnerable dependencies
            if self.check_if_vulnerable(dep):
                latest_version = self.get_latest_safe_version(dep)
                if latest_version and latest_version != dep['version']:
                    self.vulnerabilities.append({
                        'package': group_artifact,
                        'ecosystem': 'maven',
                        'current_version': dep['version'],
                        'patched_version': latest_version,
                        'cve': 'Unknown',
                        'severity': 'Medium',
                        'description': f'Outdated version of {group_artifact}',
                        'cvss_score': 5.0
                    })
        
        print(f"Manual scan complete. Found {len(self.vulnerabilities)} potential issues.")
    
    def check_if_vulnerable(self, dep: Dict) -> bool:
        """Check if a dependency is known to be vulnerable"""
        # Known vulnerable versions (simplified check)
        vulnerable_patterns = {
            'com.h2database:h2': ['2.1.', '2.2.', '2.3.'],
            'org.apache.tomcat.embed:tomcat-embed-core': ['10.0.', '10.1.0', '10.1.1'],
            'ch.qos.logback:logback': ['1.4.', '1.5.0', '1.5.1'],
            'com.fasterxml.jackson.core:jackson-databind': ['2.0.', '2.1.', '2.2.', '2.15.', '2.16.', '2.17.', '2.18.', '2.19.', '2.20.'],
        }
        
        group_artifact = f"{dep['group']}:{dep['artifact']}"
        if group_artifact in vulnerable_patterns:
            version = dep['version']
            for pattern in vulnerable_patterns[group_artifact]:
                if version.startswith(pattern):
                    return True
        
        return False
    
    def get_latest_safe_version(self, dep: Dict) -> Optional[str]:
        """Get the latest safe version of a dependency from Maven Central"""
        try:
            url = f"https://search.maven.org/solrsearch/select"
            params = {
                'q': f'g:"{dep["group"]}" AND a:"{dep["artifact"]}"',
                'rows': 1,
                'wt': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                docs = data.get('response', {}).get('docs', [])
                if docs:
                    return docs[0].get('latestVersion')
        except Exception as e:
            print(f"Warning: Could not check Maven Central for {dep['group']}:{dep['artifact']}: {e}")
        
        return None
    
    def parse_gradle_dependencies(self) -> List[Dict]:
        """Parse dependencies from build.gradle"""
        dependencies = []
        
        with open(self.build_gradle) as f:
            content = f.read()
        
        # First, extract version variables from ext block
        version_vars = {}
        # Pattern 1: set('varName', 'version')
        ext_pattern1 = r"set\(['\"](\w+)['\"],\s*['\"](.+?)['\"]\)"
        for var_name, var_value in re.findall(ext_pattern1, content):
            version_vars[var_name] = var_value
        
        # Pattern 2: varName = 'version' (in ext block or elsewhere)
        ext_pattern2 = r"(\w+Version)\s*=\s*['\"](.+?)['\"]"
        for var_name, var_value in re.findall(ext_pattern2, content):
            version_vars[var_name] = var_value
        
        # Extract dependency declarations
        dep_pattern = r"(implementation|testImplementation|runtimeOnly|compileOnly)\s+['\"](.+?):(.+?):(.+?)['\"]"
        matches = re.findall(dep_pattern, content)
        
        for match in matches:
            scope, group, artifact, version = match
            
            # Resolve version variables (e.g., $tomcatVersion or ${tomcatVersion})
            if version.startswith('$'):
                # Remove $ and optional {} brackets
                var_name = version.lstrip('$').strip('{}')
                version = version_vars.get(var_name, version)
            
            dependencies.append({
                'scope': scope,
                'group': group,
                'artifact': artifact,
                'version': version
            })
        
        return dependencies
    
    def analyze_vulnerabilities(self):
        """Analyze and deduplicate vulnerability scan results"""
        if not self.vulnerabilities:
            print("No vulnerabilities detected.")
            return
        
        # Deduplicate by package name
        seen = set()
        unique_vulns = []
        
        for vuln in self.vulnerabilities:
            key = f"{vuln['package']}:{vuln.get('cve', 'unknown')}"
            if key not in seen:
                seen.add(key)
                unique_vulns.append(vuln)
        
        self.vulnerabilities = unique_vulns
        
        print(f"Found {len(self.vulnerabilities)} unique vulnerabilities:")
        for vuln in self.vulnerabilities:
            print(f"  - {vuln['package']}: {vuln.get('cve', 'Unknown CVE')} (Severity: {vuln.get('severity', 'Unknown')})")
            print(f"    Current: {vuln.get('current_version', 'Unknown')}, Fix: {vuln.get('patched_version', 'Unknown')}")
    
    def fix_vulnerabilities(self):
        """Apply fixes for identified vulnerabilities"""
        print("Applying fixes to build.gradle...")
        
        # Read current build.gradle
        with open(self.build_gradle) as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes based on vulnerabilities found
        for vuln in self.vulnerabilities:
            package = vuln['package']
            patched_version = vuln.get('patched_version', 'Unknown')
            
            if patched_version == 'Unknown' or not patched_version:
                print(f"⚠️  No patched version available for {package}, skipping...")
                continue
            
            # Try to update the version in build.gradle
            success = self.update_dependency_version(content, package, patched_version)
            
            if success:
                content = success
                self.fixes_applied.append({
                    'package': package,
                    'old_version': vuln.get('current_version', 'Unknown'),
                    'new_version': patched_version,
                    'cve': vuln.get('cve', 'Unknown')
                })
                print(f"✅ Updated {package} to {patched_version}")
            else:
                print(f"⚠️  Could not auto-update {package}")
        
        # Write updated content if changes were made
        if content != original_content:
            with open(self.build_gradle, 'w') as f:
                f.write(content)
            print(f"\n✅ Applied {len(self.fixes_applied)} fixes to build.gradle")
        else:
            print("\n⚠️  No changes were made to build.gradle")
    
    def update_dependency_version(self, content: str, package: str, new_version: str) -> Optional[str]:
        """Update a dependency version in build.gradle content"""
        # Parse package (e.g., "com.h2database:h2" -> group="com.h2database", artifact="h2")
        if ':' in package:
            parts = package.split(':')
            group = parts[0]
            artifact = parts[1]
        else:
            # Try to match by artifact name only
            artifact = package
            group = None
        
        # Pattern 1: Direct dependency declaration with version
        # e.g., implementation 'com.h2database:h2:2.1.214'
        if group:
            pattern1 = rf"(['\"]){re.escape(group)}:{re.escape(artifact)}:[\d.]+(['\"])"
            replacement1 = rf"\1{group}:{artifact}:{new_version}\2"
            new_content = re.sub(pattern1, replacement1, content)
            if new_content != content:
                return new_content
        
        # Pattern 2: Variable-based version in ext block
        # e.g., set('h2Version', '2.1.214')
        artifact_var = f"{artifact.replace('-', '')}Version"
        pattern2 = rf"set\(['\"]({artifact_var})['\"],\s*['\"][\d.]+['\"]\)"
        replacement2 = rf"set('\1', '{new_version}')"
        new_content = re.sub(pattern2, replacement2, content)
        if new_content != content:
            return new_content
        
        # Pattern 3: Direct variable assignment
        # e.g., tomcatVersion = '10.1.20'
        pattern3 = rf"({artifact_var}\s*=\s*['\"])[\d.]+(['\"])"
        replacement3 = rf"\1{new_version}\2"
        new_content = re.sub(pattern3, replacement3, content)
        if new_content != content:
            return new_content
        
        return None
    
    def verify_build(self) -> bool:
        """Run Gradle build and tests to verify fixes"""
        print("Running './gradlew clean build --no-daemon'...")
        
        try:
            result = subprocess.run(
                ["./gradlew", "clean", "build", "--no-daemon"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                print("Build failed!")
                print("STDOUT:", result.stdout[-1000:])
                print("STDERR:", result.stderr[-1000:])
                return False
            
            print("Build successful!")
            
            # Check if tests passed
            if "BUILD SUCCESSFUL" in result.stdout:
                print("All tests passed!")
                return True
            else:
                print("Build completed but status unclear")
                return "BUILD FAILED" not in result.stdout
                
        except subprocess.TimeoutExpired:
            print("Build timed out after 10 minutes")
            return False
        except Exception as e:
            print(f"Error running build: {e}")
            return False
    
    def generate_report(self):
        """Generate a summary report of fixes"""
        report_file = self.project_root / "CVE_FIX_REPORT.md"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        with open(report_file, 'w') as f:
            f.write("# CVE Vulnerability Fix Report\n\n")
            f.write(f"**Generated:** {timestamp}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Vulnerabilities Detected:** {len(self.vulnerabilities)}\n")
            f.write(f"- **Fixes Applied:** {len(self.fixes_applied)}\n")
            f.write(f"- **Build Status:** ✅ Successful\n")
            f.write(f"- **Tests Status:** ✅ Passed\n\n")
            
            if self.vulnerabilities:
                f.write("## 🔍 Vulnerabilities Detected\n\n")
                f.write("| Package | CVE | Severity | Current Version | Fixed Version |\n")
                f.write("|---------|-----|----------|-----------------|---------------|\n")
                
                for vuln in self.vulnerabilities:
                    package = vuln.get('package', 'Unknown')
                    cve = vuln.get('cve', 'Unknown')
                    severity = vuln.get('severity', 'Unknown')
                    current = vuln.get('current_version', 'Unknown')
                    patched = vuln.get('patched_version', 'Unknown')
                    
                    f.write(f"| {package} | {cve} | {severity} | {current} | {patched} |\n")
                
                f.write("\n")
            
            if self.fixes_applied:
                f.write("## ✅ Fixes Applied\n\n")
                f.write("The following dependencies were updated to fix vulnerabilities:\n\n")
                
                for fix in self.fixes_applied:
                    package = fix.get('package', 'Unknown')
                    old_ver = fix.get('old_version', 'Unknown')
                    new_ver = fix.get('new_version', 'Unknown')
                    cve = fix.get('cve', 'Unknown')
                    
                    f.write(f"### {package}\n")
                    f.write(f"- **CVE:** {cve}\n")
                    f.write(f"- **Version Update:** {old_ver} → {new_ver}\n\n")
            
            f.write("## 🔧 Verification\n\n")
            f.write("All fixes have been verified with:\n")
            f.write("```bash\n")
            f.write("./gradlew clean build --no-daemon\n")
            f.write("```\n\n")
            f.write("- ✅ Build completed successfully\n")
            f.write("- ✅ All tests passed\n\n")
            
            f.write("---\n")
            f.write("*This report was automatically generated by the CVE Scanner*\n")
        
        print(f"📄 Report generated: {report_file}")
    
    def create_pull_request(self):
        """Create a GitHub Pull Request with the fixes"""
        print("Creating Pull Request...")
        
        # First, check if there are any changes to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            print("⚠️  No changes to commit, skipping PR creation")
            return
        
        # Create a new branch
        branch_name = f"security/fix-cves-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            # Configure git
            subprocess.run(["git", "config", "user.name", "CVE Scanner Bot"], cwd=self.project_root, check=True)
            subprocess.run(["git", "config", "user.email", "cve-scanner@github.com"], cwd=self.project_root, check=True)
            
            # Create and checkout new branch
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.project_root, check=True)
            
            # Stage changes
            subprocess.run(["git", "add", "build.gradle", "CVE_FIX_REPORT.md"], cwd=self.project_root, check=True)
            
            # Commit changes
            commit_msg = f"fix: Update dependencies to fix {len(self.fixes_applied)} CVE(s)"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.project_root, check=True)
            
            # Push to remote
            subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=self.project_root, check=True)
            
            # Create PR using GitHub CLI
            pr_title = f"[Security] Fix {len(self.fixes_applied)} CVE vulnerability(ies)"
            pr_body = self.generate_pr_body()
            
            subprocess.run(
                ["gh", "pr", "create", "--title", pr_title, "--body", pr_body, "--base", "master"],
                cwd=self.project_root,
                check=True
            )
            
            print(f"✅ Pull Request created successfully on branch '{branch_name}'")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error creating PR: {e}")
            print("Changes have been committed locally but PR creation failed.")
            print("You can manually create a PR from the branch:", branch_name)
    
    def generate_pr_body(self) -> str:
        """Generate PR description"""
        body = "## 🔒 Security Updates\n\n"
        body += "This PR automatically fixes identified CVE vulnerabilities in project dependencies.\n\n"
        
        body += f"### Summary\n"
        body += f"- **Vulnerabilities Fixed:** {len(self.fixes_applied)}\n"
        body += f"- **Build Status:** ✅ Passing\n"
        body += f"- **Tests Status:** ✅ All Passing\n\n"
        
        if self.fixes_applied:
            body += "### Changes\n\n"
            for fix in self.fixes_applied:
                package = fix.get('package', 'Unknown')
                old_ver = fix.get('old_version', 'Unknown')
                new_ver = fix.get('new_version', 'Unknown')
                cve = fix.get('cve', 'Unknown')
                body += f"- **{package}**: {old_ver} → {new_ver} (fixes {cve})\n"
            body += "\n"
        
        body += "### Verification\n\n"
        body += "✅ All changes have been verified with:\n"
        body += "```bash\n"
        body += "./gradlew clean build --no-daemon\n"
        body += "```\n\n"
        
        body += "📄 See `CVE_FIX_REPORT.md` for detailed information.\n\n"
        body += "---\n"
        body += "*This PR was automatically created by the CVE Scanner workflow.*\n"
        
        return body


def main():
    """Main entry point"""
    # Get project root (one level up from scripts directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent if script_dir.name == 'scripts' else script_dir
    
    # Create and run scanner
    scanner = CVEScanner(str(project_root))
    return scanner.run()


if __name__ == "__main__":
    sys.exit(main())
