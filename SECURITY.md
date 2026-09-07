# Security & Vulnerability Disclosure Policy

## Supported Versions

The following release branches are actively monitored and supported with security patches:

| Version | Supported          | Security Maintenance Tier |
| :------ | :----------------: | :------------------------ |
| 1.0.x   | :white_check_mark: | Primary Production Baseline |
| < 1.0   | :x:                | Deprecated / EOL          |

---

## Reporting a Security Vulnerability

We prioritize the security and defensive integrity of **OpenSentinel** above all else. If you discover a security defect, privilege escalation, telemetry interception, or credential leakage vector, please follow our coordinated disclosure policy:

> [!CAUTION]
> **DO NOT** create public GitHub Issues, Discussions, or Pull Requests for unpatched security vulnerabilities.

### Coordinated Disclosure Channel
Please submit full vulnerability details directly to our security engineering team:
- **Primary Security Contact:** `security@trujillomingorance.com`
- **Secondary Maintainer:** `alberto@trujillomingorance.com`

### Submission Guidelines
When reporting a finding, please include:
1. **Attack Vector / Scenario:** Detailed description of the vulnerability mechanism.
2. **Reproduction Steps:** Step-by-step instructions or minimal non-destructive proof-of-concept.
3. **Affected Components:** Core telemetry engine, notifiers (Discord, Telegram, WhatsApp), or Web UI.
4. **Remediation Suggestion:** Any suggested defensive architectural fixes (if known).

---

## Response & Resolution SLAs

Our security operations adhere to strict operational timelines:
- **Initial Acknowledgment:** Within **24 hours** of report receipt.
- **Triage & Severity Assessment:** Within **48 hours**.
- **Remediation & Patch Deployment:** Target of **72 hours** for critical severity CVEs.

We appreciate the efforts of security researchers practicing responsible disclosure and will publicly acknowledge contributions in release security bulletins upon mutual agreement.
