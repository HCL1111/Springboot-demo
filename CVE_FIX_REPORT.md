# CVE Vulnerability Fix Report

**Generated:** 2026-11-02 04:05:56 UTC

---

## 📊 Summary

- **Vulnerabilities Detected:** 38
- **Fixes Applied:** 38
- **Build Status:** ✅ Successful
- **Tests Status:** ✅ Passed

## 🔍 Vulnerabilities Detected

| Package | CVE | Severity | Current Version | Fixed Version |
|---------|-----|----------|-----------------|---------------|
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-5m62-pw8w-7w9f | CRITICAL | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-5mp6-jrq3-r938 | HIGH | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-69cc-cv78-qc8g | HIGH | 10.1.52 | 9.0.116 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-8mc5-53m5-3qj2 | MODERATE | 10.1.52 | 9.0.116 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-9m3c-qcxr-9x87 | MODERATE | 10.1.52 | 9.0.116 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-9m89-8frq-c98c | LOW | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-9xv2-5v5q-p794 | CRITICAL | 10.1.52 | 11.0.25 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-fv25-8xcx-gqjc | HIGH | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-gcx9-497g-6cp6 | CRITICAL | 10.1.52 | 11.0.25 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-gx5v-xp9w-j4cg | HIGH | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-h3x4-894j-xpx5 | CRITICAL | 10.1.52 | 11.0.25 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-h6fc-48rj-7qqh | CRITICAL | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-r29c-68gh-xp6x | CRITICAL | 10.1.52 | 9.0.118 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-rv64-5gf8-9qq8 | HIGH | 10.1.52 | 9.0.116 |
| org.apache.tomcat.embed:tomcat-embed-core | GHSA-x4m4-345f-5h5g | HIGH | 10.1.52 | 9.0.117 |
| ch.qos.logback:logback-core | GHSA-jhq6-gfmj-v8fx | LOW | 1.5.32 | 1.5.34 |
| ch.qos.logback:logback-core | GHSA-p47f-322f-whfh | LOW | 1.5.32 | 1.5.33 |
| org.apache.logging.log4j:log4j-core | GHSA-3pxv-7cmr-fjr4 | MODERATE | 2.25.3 | 2.25.4 |
| org.apache.logging.log4j:log4j-core | GHSA-445c-vh5m-36rj | MODERATE | 2.25.3 | 2.25.4 |
| org.apache.logging.log4j:log4j-core | GHSA-6hg6-v5c8-fphq | MODERATE | 2.25.3 | 2.25.4 |
| org.apache.logging.log4j:log4j-core | GHSA-h383-gmxw-35v2 | MODERATE | 2.25.3 | 2.25.4 |
| org.apache.logging.log4j:log4j-api | GHSA-qv9r-c865-cp47 | MODERATE | 2.25.3 | 2.25.5 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-3pjw-73gf-8qr5 | MODERATE | 2.21.1 | 2.18.8 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-5gvw-p9qm-jgwh | MODERATE | 2.21.1 | 2.21.5 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-5hh8-q8hv-fr38 | MODERATE | 2.21.1 | 2.21.4 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-5jmj-h7xm-6q6v | MODERATE | 2.21.1 | 3.1.4 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-9fxm-vc8v-hj55 | MODERATE | 2.21.1 | 2.21.4 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-cxp5-3px4-pw24 | HIGH | 2.21.1 | 2.21.7 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-gx83-3vf8-gh7j | MODERATE | 2.21.1 | 2.18.10 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-hgj6-7826-r7m5 | MODERATE | 2.21.1 | 2.18.8 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-j3rv-43j4-c7qm | HIGH | 2.21.1 | 2.18.8 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-mhm7-754m-9p8w | MODERATE | 2.21.1 | 2.18.9 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-q4xh-88c3-wmh7 | HIGH | 2.21.1 | 2.18.10 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-rcqc-6cw3-h962 | MODERATE | 2.21.1 | 2.21.4 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-rmj7-2vxq-3g9f | HIGH | 2.21.1 | 2.18.8 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-vvgp-rfg2-7rr6 | MODERATE | 2.21.1 | 2.18.9 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-wjgm-6hv5-3cvf | MODERATE | 2.21.1 | 2.18.10 |
| com.fasterxml.jackson.core:jackson-databind | GHSA-wv8q-qhhj-9h54 | HIGH | 2.21.1 | 2.18.11 |

## ✅ Fixes Applied

The following dependencies were updated to fix vulnerabilities:

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-5m62-pw8w-7w9f
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-5mp6-jrq3-r938
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-69cc-cv78-qc8g
- **Version Update:** 10.1.52 → 9.0.116

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-8mc5-53m5-3qj2
- **Version Update:** 10.1.52 → 9.0.116

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-9m3c-qcxr-9x87
- **Version Update:** 10.1.52 → 9.0.116

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-9m89-8frq-c98c
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-9xv2-5v5q-p794
- **Version Update:** 10.1.52 → 11.0.25

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-fv25-8xcx-gqjc
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-gcx9-497g-6cp6
- **Version Update:** 10.1.52 → 11.0.25

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-gx5v-xp9w-j4cg
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-h3x4-894j-xpx5
- **Version Update:** 10.1.52 → 11.0.25

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-h6fc-48rj-7qqh
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-r29c-68gh-xp6x
- **Version Update:** 10.1.52 → 9.0.118

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-rv64-5gf8-9qq8
- **Version Update:** 10.1.52 → 9.0.116

### org.apache.tomcat.embed:tomcat-embed-core
- **CVE:** GHSA-x4m4-345f-5h5g
- **Version Update:** 10.1.52 → 9.0.117

### ch.qos.logback:logback-core
- **CVE:** GHSA-jhq6-gfmj-v8fx
- **Version Update:** 1.5.32 → 1.5.34

### ch.qos.logback:logback-core
- **CVE:** GHSA-p47f-322f-whfh
- **Version Update:** 1.5.32 → 1.5.33

### org.apache.logging.log4j:log4j-core
- **CVE:** GHSA-3pxv-7cmr-fjr4
- **Version Update:** 2.25.3 → 2.25.4

### org.apache.logging.log4j:log4j-core
- **CVE:** GHSA-445c-vh5m-36rj
- **Version Update:** 2.25.3 → 2.25.4

### org.apache.logging.log4j:log4j-core
- **CVE:** GHSA-6hg6-v5c8-fphq
- **Version Update:** 2.25.3 → 2.25.4

### org.apache.logging.log4j:log4j-core
- **CVE:** GHSA-h383-gmxw-35v2
- **Version Update:** 2.25.3 → 2.25.4

### org.apache.logging.log4j:log4j-api
- **CVE:** GHSA-qv9r-c865-cp47
- **Version Update:** 2.25.3 → 2.25.5

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-3pjw-73gf-8qr5
- **Version Update:** 2.21.1 → 2.18.8

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-5gvw-p9qm-jgwh
- **Version Update:** 2.21.1 → 2.21.5

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-5hh8-q8hv-fr38
- **Version Update:** 2.21.1 → 2.21.4

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-5jmj-h7xm-6q6v
- **Version Update:** 2.21.1 → 3.1.4

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-9fxm-vc8v-hj55
- **Version Update:** 2.21.1 → 2.21.4

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-cxp5-3px4-pw24
- **Version Update:** 2.21.1 → 2.21.7

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-gx83-3vf8-gh7j
- **Version Update:** 2.21.1 → 2.18.10

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-hgj6-7826-r7m5
- **Version Update:** 2.21.1 → 2.18.8

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-j3rv-43j4-c7qm
- **Version Update:** 2.21.1 → 2.18.8

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-mhm7-754m-9p8w
- **Version Update:** 2.21.1 → 2.18.9

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-q4xh-88c3-wmh7
- **Version Update:** 2.21.1 → 2.18.10

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-rcqc-6cw3-h962
- **Version Update:** 2.21.1 → 2.21.4

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-rmj7-2vxq-3g9f
- **Version Update:** 2.21.1 → 2.18.8

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-vvgp-rfg2-7rr6
- **Version Update:** 2.21.1 → 2.18.9

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-wjgm-6hv5-3cvf
- **Version Update:** 2.21.1 → 2.18.10

### com.fasterxml.jackson.core:jackson-databind
- **CVE:** GHSA-wv8q-qhhj-9h54
- **Version Update:** 2.21.1 → 2.18.11

## 🔧 Verification

All fixes have been verified with:
```bash
./gradlew clean build --no-daemon
```

- ✅ Build completed successfully
- ✅ All tests passed

---
*This report was automatically generated by the CVE Scanner*
