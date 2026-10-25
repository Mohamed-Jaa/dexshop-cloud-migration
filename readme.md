# 🛒 DexShop — Cloud Migration & DevSecOps Production Architecture

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey?logo=flask)
![AWS](https://img.shields.io/badge/Cloud-AWS%20(EC2%20%7C%20RDS%20%7C%20S3%20%7C%20IAM)-orange?logo=amazon-aws)
![Docker](https://img.shields.io/badge/Containerization-Docker%20%26%20Compose-2496ED?logo=docker)
![Redis](https://img.shields.io/badge/Cache-Redis-DC382D?logo=redis)
![Nginx](https://img.shields.io/badge/Proxy-Nginx%20%2B%20SSL-009639?logo=nginx)
![CI/CD](https://img.shields.io/badge/DevSecOps-14--Stage%20Pipeline-success?logo=githubactions)

## 📌 Project Overview
**DexShop** is an AI-powered e-commerce web application built with **Python (Flask)**. This repository documents the complete **Cloud Migration** of the platform from a basic PaaS hosting environment (Render) to a decoupled, hardened, and highly automated **Amazon Web Services (AWS)** production infrastructure. The project leverages containerization (**Docker Compose**) and enforces strict software supply-chain security through an automated **14-Stage DevSecOps CI/CD Pipeline**.

---

## 🏗️ Production Architecture Diagram

![DexShop Production Architecture](dex_Architect.png)

---

## 🚀 Key Engineering Milestones

### 1. Code Refactoring & AI-Powered Catalog Engine
* **Application & UI Modernization:** Refactored the core Python codebase to adhere to clean architecture and PEP8 standards, paired with a responsive, modernized user interface.
* **Automated AI Product Onboarding:** Integrated an **AI Product Engine** directly into the catalog management workflow. By providing either a **product name** or uploading a **product image**, the system automatically:
  1. Extracts detailed technical specifications and product attributes.
  2. Generates structured, SEO-friendly product descriptions.
  3. Suggests an estimated market price dynamically.

---

### 2. Cloud Infrastructure & Service Decoupling (AWS)
* **Containerized Compute (`AWS EC2` & `Docker Compose`):** Hosted on an Ubuntu-based AWS EC2 instance where all application services run in isolated containers managed via Docker Compose.
* **Reverse Proxy & Concurrency (`Nginx` & `Gunicorn`):**
  * **Nginx** acts as the front-facing reverse proxy on ports `80` and `443`, handling incoming client connections and SSL termination.
  * **Gunicorn** serves the Flask application using a multi-worker WSGI model to handle concurrent requests efficiently.
* **Managed Relational Database (`Amazon RDS`):** Decoupled the database layer from the compute instance by migrating to an isolated **Amazon RDS** instance, restricted exclusively to internal traffic from the application server.
* **Stateless Media Storage (`Amazon S3`):** Offloaded all user-uploaded product images to **Amazon S3**, ensuring the application containers remain completely stateless and preserving local EC2 disk capacity.
* **In-Memory Caching Layer (`Redis`):** Deployed a dedicated **Redis** container to cache high-frequency database queries (such as `featured_products`) with a **60-second TTL**, significantly reducing RDS read load and improving response times.
* **Dynamic DNS & Automated SSL (`DuckDNS` & `Let's Encrypt`):**
  * Mapped the infrastructure to `dexshop-app.duckdns.org` with automated IP synchronization to maintain availability across dynamic EC2 IP changes.
  * Secured all HTTP traffic with **Let's Encrypt SSL/TLS** certificates configured for automated renewal every **90 days**.

---

### 3. Automated Disaster Recovery & IAM Governance
* **Scheduled Daily Database Backups:** Configured an automated **Cron Job** executing daily at **03:00 AM** to dump the production RDS database, compress the archive, and upload it to a dedicated **Amazon S3 Backup Vault**.
* **Lifecycle & Retention Policy:** Implemented an automated **30-day retention policy** that prunes backups older than 30 days to optimize storage costs.
* **Strict IAM Least-Privilege Access:** Enforced **AWS IAM** policies separating backup write operations from read operations, ensuring **only Administrators** possess read and restore permissions for the backup vault.

---

### 4. Host & Network Security Hardening
* **Firewall Isolation (`UFW` & `ufw-docker`):** Locked down host network interfaces using UFW paired with `ufw-docker` to prevent Docker from bypassing iptables rules, exposing only ports `80`, `443`, and `22`.
* **Intrusion Prevention (`Fail2ban`):** Configured custom Fail2ban jails monitoring SSH authentication logs:
  * Automatically bans offending IP addresses for **5 minutes (300 seconds)** after **8 failed login attempts**.
  * Supports trusted IP whitelisting (`ignoreip`) to prevent accidental lockouts during administrative operations.

---

### 5. 14-Stage DevSecOps CI/CD Pipeline (GitHub Actions)
Every `git push` to the `main` branch triggers an automated **14-stage security and deployment pipeline** before any code reaches production:

| Stage | Security / Deployment Check | Tool | Purpose |
| :--- | :--- | :--- | :--- |
| **1** | **Secrets Detection** | `Gitleaks` | Scans source code and Git history to prevent hardcoded API keys, tokens, or credentials. |
| **2** | **Code Quality & Linting** | `Flake8` | Enforces Python coding standards, syntax cleanliness, and PEP8 compliance. |
| **3** | **SAST Scan** | `Bandit` | Performs Static Application Security Testing on Python code to identify security vulnerabilities. |
| **4** | **SCA Scan** | `pip-audit` | Audits third-party dependencies in `requirements.txt` against known CVE databases. |
| **5** | **IaC Scan** | `Hadolint` | Lints the `Dockerfile` to enforce container security and build best practices. |
| **6** | **License Compliance** | `License Check` | Verifies open-source package licenses to prevent legal or compliance conflicts. |
| **7** | **Container Vulnerability Scan** | `Trivy` | Scans the built Docker image for OS-level and package vulnerabilities before publishing. |
| **8** | **SBOM Generation** | `Syft` | Generates a Software Bill of Materials documenting all components inside the container image. |
| **9** | **SLSA Provenance** | `SLSA` | Produces verifiable build provenance metadata to protect against supply-chain tampering. |
| **10** | **Container Image Signing** | `Cosign` | Cryptographically signs the Docker image to guarantee authenticity and integrity. |
| **11** | **Policy as Code** | `Conftest` | Validates configuration files against predefined Open Policy Agent (OPA) security rules. |
| **12** | **DAST Scan** | `OWASP ZAP` | Executes Dynamic Application Security Testing against a live ephemeral instance to detect runtime flaws. |
| **13** | **Publish to Registry (CD)** | `Docker Hub` | Pushes the verified, signed production container image to Docker Hub. |
| **14** | **Automated Production Deploy** | `SSH Action` | Connects to AWS EC2 via `dexshop-app.duckdns.org`, pulls the latest image, and updates the Docker Compose stack with zero manual intervention. |

---

## 🛠️ Operations & Maintenance Commands

```bash
# 1. Check the status of all running containers
sudo docker compose ps

# 2. Inspect active Redis cache keys and verify TTL countdown
sudo docker compose exec dexshop-redis redis-cli keys "*"
sudo docker compose exec dexshop-redis redis-cli ttl featured_products

# 3. Stream real-time application and Nginx logs
sudo docker compose logs -f

# 4. Monitor Fail2ban SSH jail status and active bans
sudo fail2ban-client status sshd
```

---

## 🔮 Future Roadmap
* **Global Edge Caching (`Amazon CloudFront`):** Place CloudFront CDN in front of Nginx and S3 for global edge caching and DDoS mitigation upon AWS account verification completion.
* **Network Isolation (`Custom VPC`):** Migrate the EC2 application tier into a **Private Subnet** behind an Application Load Balancer (ALB) with Multi-AZ RDS deployment.
* **Observability Stack:** Integrate centralized resource and application monitoring using **Prometheus & Grafana** or **AWS CloudWatch**.
