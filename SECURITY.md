Security Policy

Supported Versions

Security fixes are currently intended for the latest version on the default branch. Older versions may not receive security updates.

Reporting a Vulnerability

Please do not publish access tokens, private repository URLs, personal data, or exploit details in a public issue.

Report suspected security vulnerabilities privately to the repository maintainer through GitHub’s private vulnerability reporting feature, if enabled. If private reporting is unavailable, contact the maintainer through a private GitHub channel and include:

• A clear description of the issue and its impact.
• Steps to reproduce the issue, using a test account and non-sensitive data.
• Any relevant logs with tokens, cookies, authorization headers, and personal information removed.

You should receive an acknowledgement when the report has been reviewed. Please allow reasonable time for investigation and a fix before publicly disclosing the issue.

Token and Credential Safety

• Never commit GitHub tokens, API keys, cookies, or session credentials.
• Use a fine-grained GitHub token with access only to the required repository and Contents: Read-only permission when the userscript only needs to fetch solutions.
• Store credentials in Tampermonkey’s storage; do not paste them into issues, screenshots, source code, or logs.
• Revoke and replace any credential that may have been exposed.
• Do not use a token belonging to someone else or request broader permissions than the feature needs.

Scope and Responsible Use

Use this project only with repositories and accounts you are authorized to access. Follow GitHub’s and LeetCode’s applicable terms and rules. The project is provided without guarantees; review code before running it.