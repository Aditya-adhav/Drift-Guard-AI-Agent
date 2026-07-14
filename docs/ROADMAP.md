# Drift-Guard AI Agent - Project Roadmap

This roadmap outlines the optimal path for scaling Drift-Guard from a prototype into an enterprise-ready GitOps & IaC security tool.

## Phase 1: Core Robustness & Privacy (Immediate Next Steps)
These are the most critical features to ensure the app is safe, reliable, and handles real-world Terraform environments.

- `[x]` **Data Sanitization & Redaction:** Implement a filtering mechanism in `detector.py` to strip out sensitive keys (e.g., `password`, `secret_key`, `token`) from the Terraform JSON state before sending it to the LLM.
- `[x]` **Multi-File Support:** Currently, the app assumes all code is in `main.tf`. Real projects use multiple files (`variables.tf`, `outputs.tf`, modules, etc.). Update the AI prompt to read the entire directory and allow the AI to specify *which* file needs the fix.
- `[ ]` **Git Integration (Pull Requests):** Instead of immediately overwriting the local file, integrate with Git (via `GitPython`) or GitHub API to create a new branch and raise a Pull Request with the AI's proposed HCL fix. This aligns perfectly with GitOps best practices.

## Phase 2: Advanced AI Remediation & Insights
Enhancing how the AI interacts with the user and the code.

- [ ] **Multiple Remediation Strategies:** Sometimes the right answer isn't to fix the code, but to ignore the drift. Give the AI the ability to suggest adding a `lifecycle { ignore_changes = [...] }` block.
- [ ] **Drift Cost Impact Analysis:** Integrate with tools like Infracost to calculate exactly how much money the manual cloud change is costing the company, and display it in the UI.
- [ ] **Context-Aware Modules:** Allow the AI to read custom Terraform modules so it understands the full architectural context, rather than just the top-level resources.

## Phase 3: Operationalizing the Agent
Making the tool something that can run in the background in a production environment.

- [x] **Dockerization:** Containerize the application including its Python and Terraform dependencies so it can be deployed consistently anywhere.
- [ ] **Headless/Background Scanning:** Move away from the Streamlit UI's `time.sleep` loop for continuous scanning. Implement a proper background scheduler (like Celery or APScheduler) that runs as a daemon.
- [ ] **Alerting & Notifications:** Add Webhook support so when drift is detected, it sends a Slack, Microsoft Teams, or Discord message with a summary of the drift and a link to the dashboard to approve the AI's fix.
- [ ] **Audit Logging:** Keep a local SQLite database of all historical drifts, AI categorizations, and which user approved or rejected the AI's fix.

## Phase 4: Scaling the Ecosystem
Expanding the scope of what Drift-Guard can protect.

- [ ] **Support for Other IaC Tools:** Abstract the underlying logic so it can support Pulumi, AWS CloudFormation, or Kubernetes Manifests, in addition to Terraform.
- [ ] **Multi-Workspace Support:** Allow users to define multiple environments (e.g., `dev`, `staging`, `prod`) and monitor them all from a single dashboard.
- [ ] **RBAC / Authentication:** Add a login screen to the Streamlit app so that only authorized DevOps engineers can approve HCL code changes or revert infrastructure.
