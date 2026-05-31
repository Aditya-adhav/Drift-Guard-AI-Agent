# Drift-Guard AI Agent 🛡️

Drift-Guard is an **Agentic Cloud Guardian** and digital twin for your Infrastructure as Code (IaC). It continuously monitors your cloud infrastructure for configuration drift using Terraform. When drift is detected, it uses advanced LLM reasoning to categorize the risk (Security, Cost, Neutral) and automatically generates corrected HCL (HashiCorp Configuration Language) code to remediate the drift.

## Features
- **Continuous Monitoring**: Scans your Terraform state against the live cloud environment.
- **AI Remediation**: Uses LLMs (OpenAI, Groq, or local models via Ollama) to analyze Terraform plan diffs.
- **Self-Correcting**: Automatically generates valid HCL code to fix the drift, validating it before proposing the fix.
- **Human-in-the-Loop**: Review the proposed HCL code via a premium Streamlit UI before applying it or reverting the cloud changes.

---

## 🚀 Getting Started Tutorial

Follow these steps to set up the environment, install the necessary tools, and run Drift-Guard.

### 1. Install Prerequisites

#### A. Install Python
1. Download Python from the [official website](https://www.python.org/downloads/).
2. Run the installer and **make sure to check "Add Python to PATH"** at the bottom of the installation window.
3. Verify installation in your terminal:
   ```bash
   python --version
   ```

#### B. Install Terraform
1. Download Terraform for your OS from [HashiCorp's website](https://developer.hashicorp.com/terraform/downloads).
2. Extract the executable and add its folder to your system's PATH.
3. Verify installation:
   ```bash
   terraform --version
   ```

#### C. Install AWS CLI & Authenticate
Since Drift-Guard uses Terraform to check AWS infrastructure, you need the AWS CLI installed and configured.
1. Download the [AWS CLI Installer for Windows](https://awscli.amazonaws.com/AWSCLIV2.msi).
2. Run the installer.
3. Open a new terminal and log in using your AWS credentials:
   ```bash
   aws configure
   ```
4. Enter your `AWS Access Key ID`, `AWS Secret Access Key`, `Default region name` (e.g., `us-east-1`), and `Default output format` (e.g., `json`).

### 2. Set Up the LLM (Large Language Model)
Drift-Guard needs an AI model to reason about the infrastructure drift. You have two main options:

**Option A: Cloud Providers (OpenAI, Groq)**
- Simply get an API key from [OpenAI](https://platform.openai.com/) or [Groq](https://console.groq.com/).
- You will paste this key directly into the Drift-Guard UI later.

**Option B: Local Open-Source Models (Ollama)**
- Download and install [Ollama](https://ollama.com/).
- Run a model locally in your terminal (e.g., Qwen 2.5 Coder):
  ```bash
  ollama run qwen2.5-coder:7b
  ```
- Leave Ollama running. The base URL for the app will be `http://localhost:11434/v1`.

### 3. Install Project Dependencies
Navigate to the Drift-Guard project folder in your terminal and install the required Python libraries:

```bash
cd c:\Users\adity\OneDrive\Desktop\drift
pip install -r requirements.txt
```

### 4. Initialize Terraform
Before running the agent, initialize Terraform in your project folder so it downloads the necessary providers (like AWS):

```bash
terraform init
```

### 5. Run the Drift-Guard Agent
Launch the beautiful Streamlit web interface:

```bash
streamlit run app.py
```

### 6. Using the App
1. The web interface will automatically open in your browser (usually `http://localhost:8501`).
2. In the **sidebar**, configure your LLM settings:
   - **LLM API Key**: Enter your OpenAI/Groq key (leave blank or enter a dummy string if using Ollama).
   - **LLM Base URL**: `https://api.openai.com/v1` (OpenAI), `https://api.groq.com/openai/v1` (Groq), or `http://localhost:11434/v1` (Ollama).
   - **Model Name**: e.g., `gpt-4o`, `llama3-70b-8192`, or `qwen2.5-coder:7b`.
3. Click **Scan for Drift** to analyze your AWS environment.
4. If drift is detected, click **Trigger AI Remediation** to have the AI write the Terraform fix!

---
*Built with ❤️.*
**Made by Aditya Adhav**