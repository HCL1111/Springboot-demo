#!/usr/bin/env python3
"""
Test script for CVE Scanner and Fixer

This script tests the CVE scanner by:
1. Creating a temporary vulnerable dependency
2. Running the scanner
3. Verifying it detects and fixes the vulnerability
4. Restoring the original state
"""

import subprocess
import sys
import shutil
from pathlib import Path
import tempfile


class CVEScannerTester:
    """Test harness for CVE scanner"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.build_gradle = self.project_root / "build.gradle"
        self.backup_file = None
        self.test_passed = True
        
    def setup(self):
        """Backup original build.gradle"""
        print("=" * 80)
        print("CVE Scanner Test Suite")
        print("=" * 80)
        print("\nSetting up test environment...")
        
        self.backup_file = self.project_root / "build.gradle.test_backup"
        shutil.copy(self.build_gradle, self.backup_file)
        print(f"✅ Backed up build.gradle to {self.backup_file}")
        
    def teardown(self):
        """Restore original build.gradle"""
        print("\nCleaning up test environment...")
        
        if self.backup_file and self.backup_file.exists():
            shutil.copy(self.backup_file, self.build_gradle)
            self.backup_file.unlink()
            print("✅ Restored original build.gradle")
        
        # Clean up test artifacts
        report_file = self.project_root / "CVE_FIX_REPORT.md"
        if report_file.exists():
            report_file.unlink()
            print("✅ Removed test CVE report")
            
    def introduce_vulnerability(self):
        """Introduce a known vulnerable dependency"""
        print("\nTest 1: Introducing known vulnerable dependency...")
        
        with open(self.build_gradle) as f:
            content = f.read()
        
        # Replace H2 with a vulnerable version
        original_line = "runtimeOnly 'com.h2database:h2:2.4.240'"
        vulnerable_line = "runtimeOnly 'com.h2database:h2:2.1.214'"
        
        if original_line not in content:
            print("❌ Could not find H2 dependency in build.gradle")
            self.test_passed = False
            return False
        
        content = content.replace(original_line, vulnerable_line)
        
        with open(self.build_gradle, 'w') as f:
            f.write(content)
        
        print("✅ Introduced vulnerable H2 2.1.214 dependency")
        return True
        
    def run_scanner(self):
        """Run the CVE scanner"""
        print("\nTest 2: Running CVE scanner...")
        
        script_path = self.project_root / "scripts" / "fix_cves.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            print("Scanner output:")
            print("-" * 80)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            print("-" * 80)
            
            if result.returncode != 0:
                print(f"❌ Scanner exited with code {result.returncode}")
                self.test_passed = False
                return False
            
            print("✅ Scanner completed successfully")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Scanner timed out after 5 minutes")
            self.test_passed = False
            return False
        except Exception as e:
            print(f"❌ Error running scanner: {e}")
            self.test_passed = False
            return False
    
    def verify_fix(self):
        """Verify that the vulnerability was fixed"""
        print("\nTest 3: Verifying vulnerability was fixed...")
        
        with open(self.build_gradle) as f:
            content = f.read()
        
        # Check that vulnerable version is no longer present
        if "2.1.214" in content:
            print("❌ Vulnerable version 2.1.214 still present in build.gradle")
            self.test_passed = False
            return False
        
        # Check that a newer version was applied
        if "com.h2database:h2" not in content:
            print("❌ H2 dependency was removed instead of updated")
            self.test_passed = False
            return False
        
        print("✅ Vulnerable version was successfully updated")
        
        # Verify CVE report was generated
        report_file = self.project_root / "CVE_FIX_REPORT.md"
        if not report_file.exists():
            print("❌ CVE_FIX_REPORT.md was not generated")
            self.test_passed = False
            return False
        
        print("✅ CVE_FIX_REPORT.md was generated")
        
        # Check report contents
        with open(report_file) as f:
            report_content = f.read()
        
        if "com.h2database:h2" not in report_content:
            print("❌ Report doesn't mention H2 database fix")
            self.test_passed = False
            return False
        
        if "Fixes Applied: 1" not in report_content and "Fixes Applied:** 1" not in report_content:
            print("❌ Report doesn't show 1 fix applied")
            self.test_passed = False
            return False
        
        print("✅ CVE report contains expected fix information")
        return True
    
    def verify_build(self):
        """Verify the build still works after fix"""
        print("\nTest 4: Verifying build passes with fixed dependencies...")
        
        try:
            result = subprocess.run(
                ["./gradlew", "clean", "build", "--no-daemon"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                print("❌ Build failed after applying fixes")
                print("Last 500 chars of output:")
                print(result.stdout[-500:])
                self.test_passed = False
                return False
            
            if "BUILD SUCCESSFUL" not in result.stdout:
                print("❌ Build did not complete successfully")
                self.test_passed = False
                return False
            
            print("✅ Build passed with fixed dependencies")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Build timed out after 5 minutes")
            self.test_passed = False
            return False
        except Exception as e:
            print(f"❌ Error running build: {e}")
            self.test_passed = False
            return False
    
    def test_no_vulnerabilities(self):
        """Test scanner with no vulnerabilities"""
        print("\nTest 5: Testing scanner with no vulnerabilities...")
        
        # Restore original (secure) build.gradle
        if self.backup_file and self.backup_file.exists():
            shutil.copy(self.backup_file, self.build_gradle)
        
        script_path = self.project_root / "scripts" / "fix_cves.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                print(f"❌ Scanner failed with code {result.returncode}")
                self.test_passed = False
                return False
            
            if "No vulnerabilities found" not in result.stdout:
                print("❌ Scanner should report no vulnerabilities for current dependencies")
                self.test_passed = False
                return False
            
            print("✅ Scanner correctly reports no vulnerabilities")
            return True
            
        except Exception as e:
            print(f"❌ Error running scanner: {e}")
            self.test_passed = False
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        try:
            self.setup()
            
            # Test 1-4: Vulnerability detection and fixing
            if not self.introduce_vulnerability():
                return 1
            
            if not self.run_scanner():
                return 1
            
            if not self.verify_fix():
                return 1
            
            if not self.verify_build():
                return 1
            
            # Test 5: No vulnerabilities case
            if not self.test_no_vulnerabilities():
                return 1
            
            # All tests passed
            print("\n" + "=" * 80)
            if self.test_passed:
                print("✅ ALL TESTS PASSED!")
                print("=" * 80)
                print("\nSummary:")
                print("  ✅ Scanner can detect vulnerable dependencies")
                print("  ✅ Scanner can automatically fix vulnerabilities")
                print("  ✅ Scanner generates detailed CVE reports")
                print("  ✅ Fixed dependencies pass build and tests")
                print("  ✅ Scanner correctly handles no vulnerabilities case")
                return 0
            else:
                print("❌ SOME TESTS FAILED")
                print("=" * 80)
                return 1
                
        finally:
            self.teardown()


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent if script_dir.name == 'scripts' else script_dir
    
    tester = CVEScannerTester(str(project_root))
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
