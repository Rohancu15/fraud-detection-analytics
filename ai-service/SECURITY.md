# SECURITY.md

## Fraud Detection Analytics Security Report

### 1. SQL Injection
Risk: Malicious SQL queries can access database data.

Mitigation:
- Use prepared statements
- Use JPA queries
- Validate input

### 2. Cross Site Scripting (XSS)
Risk: JavaScript injection in forms.

Mitigation:
- Sanitize user input
- Escape frontend output

### 3. Prompt Injection
Risk: User manipulates AI prompt.

Mitigation:
- Filter suspicious text
- Limit prompt size
- Use fixed templates

### 4. Rate Limiting Abuse
Risk: Too many requests crash server.

Mitigation:
- Use flask-limiter
- 30 req/min max

### 5. Authentication Bypass
Risk: Unauthorized access.

Mitigation:
- JWT token required
- Role based access

## Summary
System secured using validation, auth, and rate limiting.