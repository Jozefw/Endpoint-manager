# Endpoint Fleet Management & Compliance Lab
## Project Runbook

### 1. Purpose

This runbook explains how to run the simulated endpoint compliance checker, generate reports, and execute automated tests.

The project currently uses fictional device inventory data. It does not collect information from real computers or require a paid MDM platform.

### 2. Project Files

| File | Purpose |
|---|---|
| `fleet.py` | Evaluates devices against compliance policy and generates reports |
| `devices.json` | Simulated endpoint inventory |
| `policy.json` | Configurable security and compliance requirements |
| `test_fleet.py` | Automated tests for compliance logic and invalid data |
| `compliance_report.csv` | Generated report containing device status, risk, and issues |
| `README.md` | Project overview and documentation |
| `RUNBOOK.md` | Operational instructions and commands |

### 3. Prerequisites

- macOS or another system with Python 3
- Terminal or a compatible command-line shell
- Git for version control
- VS Code or another text editor

The project uses Python's standard library and requires no third-party packages.

Check the installed Python version:

```bash
python3 --version
```

Check Git:

```bash
git --version
```

### 4. Navigate to the Project

Open Terminal and navigate to the project directory.

```bash
cd ~/Desktop/Endpoint
```

Confirm the current directory:

```bash
pwd
```

List the project files:

```bash
ls
```

### 5. Run the Compliance Report

Execute the main application:

```bash
python3 fleet.py
```

The application will:

1. Load `devices.json`.
2. Load `policy.json`.
3. Validate device records.
4. Evaluate each device against the policy.
5. Assign compliance status and risk level.
6. Print fleet statistics.
7. Generate `compliance_report.csv`.

Expected results with the current six-device inventory:

- Total devices: 6
- Compliant devices: 4
- Non-compliant devices: 2
- Fleet compliance: 66.7%

The two simulated failures are an encryption violation and an unsupported operating system.

### 6. Run Automated Tests

Run all discovered tests:

```bash
python3 -m unittest -v
```

The test suite checks:

- A fully compliant device
- Disabled disk encryption
- Disabled screen lock
- Unsupported operating systems
- An outdated OS version
- Multiple simultaneous issues
- Missing required fields
- Invalid OS version data

Expected result:

```text
Ran 8 tests
OK
```

The exact test output may vary slightly by Python version.

Run the test file directly if needed:

```bash
python3 test_fleet.py
```

### 7. Inspect the CSV Report

After running the compliance checker, verify that the report exists:

```bash
ls -l compliance_report.csv
```

Display the report in Terminal:

```bash
cat compliance_report.csv
```

Open the CSV in the default macOS application:

```bash
open compliance_report.csv
```

The report can also be opened in Excel or Apple Numbers.

**Important:** Running `fleet.py` overwrites the previous CSV report with the latest results.

### 8. Validate JSON Files

Check that the inventory contains valid JSON:

```bash
python3 -m json.tool devices.json
```

Check the policy file:

```bash
python3 -m json.tool policy.json
```

These commands validate JSON syntax. They do not verify every policy rule or device field.

### 9. Review Changes with Git

Check the current repository status:

```bash
git status
```

Review changes to tracked files:

```bash
git diff
```

After verifying the application and tests, stage the project changes:

```bash
git add fleet.py test_fleet.py devices.json policy.json RUNBOOK.md README.md
```

Commit the verified changes:

```bash
git commit -m "Add endpoint compliance validation and runbook"
```

If Git reports that there is nothing to commit, check `git status` before proceeding.

### 10. Recommended Verification Sequence

Run these commands from the project directory before committing changes:

```bash
python3 -m json.tool devices.json
python3 -m json.tool policy.json
python3 -m unittest -v
python3 fleet.py
ls -l compliance_report.csv
git status
```

Confirm that the JSON files parse, the tests pass, the report runs, and the CSV is generated.

### 11. Troubleshooting

**Error: `No such file or directory`**

Confirm that Terminal is in the project directory:

```bash
pwd
ls
```

**Error: `ModuleNotFoundError`**

Confirm that you are using Python 3 and that the expected project files exist. The current project should not require third-party packages.

**Error: `JSONDecodeError`**

Check the relevant JSON file for missing commas, extra commas, unquoted property names, or mismatched braces.

**Tests fail**

Read the failed test name and error message. Review the corresponding compliance rule in `fleet.py` before changing the test expectation.

**CSV report is missing**

Run the application again:

```bash
python3 fleet.py
```

Confirm that it finishes without an error and that the output includes the CSV save message.

### 12. Current Scope and Limitations

This is a local proof of concept using simulated endpoint data.

Current capabilities include configurable compliance rules, device validation, risk classification, fleet statistics, CSV reporting, and automated tests.

It does not yet provide live endpoint discovery, MDM integration, scheduled execution, or a graphical dashboard.

Those capabilities may be added in later project phases.
