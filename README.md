# Cyberlab

A containerized cybersecurity lab built with Docker Compose for hands-on learning about application security, network segmentation, centralized logging, and security detection.

## ⚠️ Warning

This project intentionally contains vulnerable application code for educational purposes. Run it only in an isolated, controlled environment. Do not expose vulnerable services to the public internet or use real credentials.

## Architecture

```text
attacker01 → web01 (Nginx) → app01 (Flask) → db01 (MariaDB)

Application and service logs
          ↓
    Grafana Alloy
          ↓
      Grafana Loki
          ↓
       Grafana
```

## Technologies

- Docker Compose
- Nginx reverse proxy
- Python and Flask
- MariaDB
- Grafana Alloy
- Grafana Loki
- Grafana

## Services

| Service | Purpose |
|---|---|
| `web01` | Nginx reverse proxy and HTTP access logs |
| `app01` | Flask application and application security exercises |
| `db01` | MariaDB database |
| `attacker01` | Lab container for security testing |
| Alloy | Collects and forwards logs |
| Loki | Centralized log storage and querying |
| Grafana | Log exploration and alerting |

## Security Exercises

### 1. SQL Injection Detection

The `/login` endpoint intentionally uses unsafe SQL string concatenation for a controlled learning exercise.

- A browser-based login form submits credentials using POST.
- Suspicious username patterns generate a warning in the application logs.
- Grafana Loki collects the warning.
- A Grafana alert detects matching events.

Example Loki query:

```logql
{service="app01"} |= "Possible SQL injection attempt"
```

Example alert query:

```logql
sum(count_over_time({service="app01"} |= "Possible SQL injection attempt" [1m]))
```

The alert is configured to fire when the query result is above zero.

### 2. Failed Login Detection

The application logs failed login attempts, including the username and source address.

Example Loki query:

```logql
{service="app01"} |= "Failed login"
```

A Grafana alert was tested using repeated failed login attempts.

### 3. Repeated HTTP 404 Detection

Detects repeated requests for missing web resources through Nginx access logs.

Example Loki query:

```logql
sum(count_over_time({service="web01"} |= " 404 " [1m]))
```

The alert threshold is set to detect more than 10 matching responses per minute.

### 4. Suspicious HTTP Request Patterns

Detects requests containing patterns associated with path traversal, SQL injection, or attempts to access environment files.

Example Loki query:

```logql
sum(count_over_time({service="web01"} |~ "(?i)(\\.\\./|union[[:space:]]+select|/\\.env)" [1m]))
```

The alert fires when matching requests are detected.

## Logging and Monitoring

The lab uses Grafana Alloy to collect service logs and Grafana Loki to store and query them. Grafana Explore can be used to inspect logs by service label.

Examples:

```logql
{service="web01"}
```

```logql
{service="app01"}
```

The SQL injection warning can be found with:

```logql
{service="app01"} |= "Possible SQL injection attempt"
```

## Network Segmentation and Hardening

The lab is designed to explore separation between application, database, and logging components.

The Flask application container also uses hardening measures such as a non-root user, dropped Linux capabilities, and a read-only root filesystem with a temporary filesystem for `/tmp`.

## Container Image Vulnerability Scanning

Scanned the cyberlab-app01:latest Docker image using Trivy.

    Scanner: Trivy 0.76.1

    Scan date: 2026-10-26

    Severity checked: HIGH

    Full scan: 44 HIGH findings

    With --ignore-unfixed: 0 HIGH findings

Findings and limitations

The full scan reported HIGH-severity findings, primarily involving operating-system packages in the base image. Trivy did not report HIGH findings with known fixes when --ignore-unfixed was used.

This does not mean the image is vulnerability-free. Findings without a reported fix may still represent security risks. Results reflect the scanner's vulnerability database at the time of the scan.
Reproduce the scan

sudo trivy image --severity HIGH cyberlab-app01:latest
sudo trivy image --severity HIGH --ignore-unfixed cyberlab-app01:latest

## Current Status

The following detections have been exercised and verified during testing:

- Failed login detection
- Repeated HTTP 404 detection
- Suspicious HTTP request pattern detection
- SQL injection warning and Grafana alert

Container Security

- Configured the app01 container to run as a non-root user.

- Applied container hardening measures, including a read-only root filesystem, dropped Linux capabilities, and a temporary filesystem for /tmp.

- Scanned the cyberlab-app01:latest image using Trivy.

- Identified remaining HIGH-severity vulnerability findings in the container image.

- Confirmed that Trivy reports zero HIGH findings when using --ignore-unfixed; the full scan still reports HIGH findings that require continued monitoring.

This is an ongoing personal cybersecurity learning project. Configuration and detection rules may evolve as additional exercises are added.
