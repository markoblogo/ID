# Security policy

Only the latest release receives security fixes.

## Data boundary

ID is a local CLI. Profile source files and generated exports remain on disk until the owner shares them. Compact and MCP resource exports require a valid matching privacy policy unless the owner explicitly selects the reviewed legacy `--allow-unfiltered` path.

Keep real private profiles outside public repositories. Use synthetic fixtures for issues, pull requests, demos, and tests. Review generated artifacts before attaching them to another tool because allowed low-risk fields can still reveal information in combination.

## Report a vulnerability

Use GitHub's private **Report a vulnerability** form in the repository Security tab. Do not include private profiles, access tokens, or exploit details in a public issue.
