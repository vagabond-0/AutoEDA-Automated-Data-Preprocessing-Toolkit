#  🔐 Security Policy

## Supported Versions

The current version of AutoEDA is under active development. Security updates will be provided for the latest release on the `main` branch.

| Version | Supported          |
|---------|--------------------|
| main    | ✅                 |
| < main  | ❌ (Not supported) |

## 🛡️ Reporting a Vulnerability

If you discover a security vulnerability in this repository, please follow these steps:

1. **Do not create a public issue.**
2. Instead, email us directly.
3. Include the following in your message:
   - A detailed description of the vulnerability
   - Steps to reproduce the issue
   - The impact of the vulnerability
   - Any suggested fixes, if available

We aim to respond within **5 business days**.

## 📃 Scope

This project is a Python-based data preprocessing toolkit and does not handle user authentication, networking, or external system integration. However, the following areas are still relevant from a security perspective:

- Malicious code execution via untrusted data
- Denial of service from malformed input data
- Dependencies with known vulnerabilities

## ✅ Security Best Practices

If you're using or contributing to AutoEDA:

- Always install dependencies using a virtual environment.
- Regularly scan your environment with tools like `pip-audit` or `safety`.
- Avoid loading or processing untrusted datasets without inspection.

## Responsible Disclosure

We encourage responsible disclosure of vulnerabilities. All reports will be thoroughly investigated, and appropriate actions will be taken to ensure the security of this project and its users.

🙏 Thank you for helping keep AutoEDA secure!
