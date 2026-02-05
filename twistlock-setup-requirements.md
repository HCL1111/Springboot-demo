# Twistlock (Prisma Cloud) Setup Requirements

## Purpose
This document outlines the information and credentials required to install and configure Twistlock CLI (`twistcli`) for vulnerability scanning and CVE fixes in our development environment.

## Required Information from ANZ

### 1. Prisma Cloud Console Details
- **Console URL**: The web address of your ANZ Prisma Cloud console
  - Format: `https://console.anz-domain.com` or `https://region.prismacloud.io`
  - Example: `https://app3.prismacloud.io` or `https://prisma.anz.example.com`

### 2. API Access Credentials
Please provide API credentials with appropriate permissions for CLI access:

- **Access Key ID** (Username)
  - Generated from Prisma Cloud Console → Settings → Access Keys
  
- **Secret Key** (Password)
  - Provided when the Access Key is created (only shown once)

- **Required Permissions**:
  - Compute → Read/Write access for vulnerability scanning
  - Code Security → Read access (if using code scanning features)

### 3. TwistCLI Download Information
- **Download Method**: One of the following:
  - [ ] Direct download URL from console: `https://<console-url>/api/v1/util/twistcli`
  - [ ] Pre-downloaded binary location (if available)
  - [ ] Installation package or installer

### 4. Additional Configuration (if applicable)
- **Proxy Settings** (if required for network access):
  - Proxy URL: `___________________________`
  - Proxy Port: `___________________________`
  - Authentication required: [ ] Yes [ ] No

- **Certificate/SSL Configuration**:
  - Custom CA certificates required: [ ] Yes [ ] No
  - Certificate location (if yes): `___________________________`

## Intended Use Cases

We plan to use Twistlock for:
- [ ] Container image vulnerability scanning
- [ ] Source code security analysis (SAST)
- [ ] Dependency vulnerability scanning (SCA)
- [ ] Infrastructure as Code scanning
- [ ] CI/CD pipeline integration

## Installation Target
- **Operating System**: Windows 11
- **Environment**: Local development machine
- **Project Type**: Java (Gradle-based Spring Boot application)

## Timeline
Please provide the above information by: **_______________**

## Contact Information
- **Requestor**: ___________________________
- **Team**: ___________________________
- **Email**: ___________________________
- **Purpose**: CVE vulnerability scanning and remediation

---

## Notes
- Credentials should be shared securely (not via plain email)
- Access keys should have appropriate least-privilege permissions
- Documentation or wiki links for ANZ-specific Twistlock setup would be helpful

## Questions?
If you have any questions about these requirements, please contact: ___________________________
