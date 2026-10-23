# Endpoint Automation Lab

A hands-on lab for learning endpoint administration, IT troubleshooting, scripting, and AI-assisted automation. The goal is to turn repetitive IT support tasks into reliable, documented, and repeatable workflows.

## Lab Objectives

- Understand endpoint configuration, health, and common support issues.
- Automate repetitive IT tasks with shell scripting and Python.
- Collect diagnostic information and produce useful troubleshooting reports.
- Explore AI-assisted troubleshooting, script development, and documentation.
- Build safe, repeatable workflows with logging, error handling, and validation.
- Create practical projects that demonstrate technical problem-solving and operational improvement.

## Curriculum

### Phase 1 — Lab Setup & Endpoint Fundamentals
- [ ] 01. [Lab Environment and Architecture](labs/01-lab-environment.md)
- [ ] 02. [Endpoint Inventory and System Information](labs/02-endpoint-inventory.md)
- [ ] 03. [Processes, Services, Storage, and System Health](labs/03-endpoint-health.md)

### Phase 2 — Troubleshooting & Diagnostics
- [ ] 04. [Network Diagnostics: DNS, DHCP, TCP/IP, and Connectivity](labs/04-network-diagnostics.md)
- [ ] 05. [Application and Process Troubleshooting](labs/05-application-troubleshooting.md)
- [ ] 06. [Logs, Events, and Root-Cause Investigation](labs/06-logs-and-events.md)

### Phase 3 — Scripting & Automation
- [ ] 07. [Shell Scripting Fundamentals](labs/07-shell-scripting.md)
- [ ] 08. [Python for IT Automation](labs/08-python-automation.md)
- [ ] 09. [Automated Endpoint Health Checks](labs/09-health-check-automation.md)
- [ ] 10. [Error Handling, Logging, and Safe Execution](labs/10-reliable-automation.md)

### Phase 4 — Endpoint Administration
- [ ] 11. [User Accounts, Permissions, and Access](labs/11-accounts-and-permissions.md)
- [ ] 12. [Software Inventory and Installation Workflows](labs/12-software-management.md)
- [ ] 13. [Configuration Checks and Endpoint Compliance](labs/13-configuration-and-compliance.md)
- [ ] 14. [Device Provisioning and Deployment Workflows](labs/14-device-provisioning.md)

### Phase 5 — AI-Assisted IT Operations
- [ ] 15. [Using AI to Investigate Technical Issues](labs/15-ai-assisted-troubleshooting.md)
- [ ] 16. [AI-Assisted Script Development and Validation](labs/16-ai-assisted-scripting.md)
- [ ] 17. [Turning Troubleshooting Steps into Reusable Runbooks](labs/17-ai-runbook-generation.md)
- [ ] 18. [Designing Human-Reviewed Automation Workflows](labs/18-ai-workflow-design.md)

### Phase 6 — Capstone Projects
- [ ] 19. [Endpoint Health Assessment Tool](labs/19-capstone-health-assessment.md)
- [ ] 20. [Automated Diagnostic Report Generator](labs/20-capstone-diagnostic-report.md)
- [ ] 21. [AI-Assisted Troubleshooting Workflow](labs/21-capstone-ai-troubleshooting.md)
- [ ] 22. [Final Project: Endpoint Support Automation Toolkit](labs/22-capstone-support-toolkit.md)

## Standard Lab Format

Each lab will include:

1. **Objective** — What you will learn and why it matters.
2. **Environment** — Required tools, operating system, and setup.
3. **Concepts** — Plain-English explanations of the technical terms.
4. **Hands-on exercise** — Commands or code to execute step by step.
5. **Expected results** — What successful execution should look like.
6. **Troubleshooting** — Common errors and how to investigate them.
7. **Automation opportunity** — How the task could be made repeatable.
8. **AI application** — Where AI helps, what it cannot safely assume, and how to validate its output.
9. **Evidence of completion** — A working result, script, report, or documented workflow.

## Project Structure

```text
endpoint-automation-lab/
├── README.md
├── labs/
│   ├── 01-lab-environment.md
│   ├── 02-endpoint-inventory.md
│   ├── 03-endpoint-health.md
│   └── ...
├── scripts/
│   ├── shell/
│   └── python/
├── reports/
├── runbooks/
├── tests/
└── docs/
    └── architecture.md
```

## Tools and Technologies

The lab will introduce tools as they become relevant:

- **Operating systems:** macOS and Windows, with Linux where useful.
- **Command line:** macOS Terminal, Bash, PowerShell, and common diagnostic utilities.
- **Automation:** Shell scripting and Python.
- **Networking:** DNS, DHCP, TCP/IP, connectivity tests, and name resolution.
- **Endpoint administration:** Processes, services, software inventory, permissions, and device configuration.
- **AI assistance:** Troubleshooting analysis, script drafting, documentation, and workflow design.
- **Quality controls:** Logging, testing, error handling, least privilege, and human review.

## Safety Rules

- Begin with read-only diagnostics before changing system configuration.
- Explain commands and their flags before running them.
- Do not expose passwords, access tokens, private keys, or sensitive customer data to AI tools.
- Test scripts in a controlled environment before using them on real endpoints.
- Require explicit review before destructive actions, permission changes, software removal, or bulk deployment.
- Record what each automation does, what it changes, and how to recover from failure.

## Progress Tracking

Mark a lab complete only after executing the exercise and verifying the expected result. Keep useful scripts, sanitized output, troubleshooting notes, and runbooks in the repository.

**Final deliverable:** A small, documented endpoint support automation toolkit that demonstrates how to investigate endpoint issues, automate repeatable tasks, and use AI responsibly to improve support workflows.