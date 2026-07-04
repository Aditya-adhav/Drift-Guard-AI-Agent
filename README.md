<div align="center">

# 🛡️ Drift-Guard AI Agent

**Agentic Cloud Guardian & Digital Twin for Infrastructure as Code**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Terraform](https://img.shields.io/badge/terraform-1.0+-623CE4.svg)](https://www.terraform.io/)
[![AWS CLI](https://img.shields.io/badge/AWS-CLI-FF9900.svg)](https://aws.amazon.com/cli/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)](https://streamlit.io/)

</div>

---

> **Drift-Guard** continuously monitors your cloud infrastructure for configuration drift using Terraform. When drift is detected, it uses advanced LLM reasoning to categorize the risk (Security, Cost, Neutral) and automatically generates corrected HCL (HashiCorp Configuration Language) code to remediate the drift.

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🔍 **Continuous Monitoring** | Scans your local Terraform state against the live cloud environment. |
| 🤖 **AI Remediation** | Uses LLMs (OpenAI, Groq, or local Ollama models) to analyze `terraform plan` diffs. |
| 🛠️ **Self-Correcting** | Automatically generates and validates HCL code to fix drift before proposing it. |
| 🧑‍💻 **Human-in-the-Loop** | Review proposed HCL fixes via a premium Streamlit UI before applying or reverting changes. |

---

## 🚀 Quick Start (Docker)

The easiest and recommended way to run Drift-Guard is using our official Docker image. This means you do **not** need to install Python or Terraform on your host machine!

### 1️⃣ Prerequisites

1. **Docker**: Ensure Docker is installed and running on your machine.
2. **AWS Credentials**: Have your AWS Access Key ID and Secret Access Key ready.
3. **An LLM**: You need an AI model to reason about the drift.
   - **Option A (Cloud)**: Get an API key from [OpenAI](https://platform.openai.com/) or [Groq](https://console.groq.com/).
   - **Option B (Local)**: Install [Ollama](https://ollama.com/) and run a local model (e.g., `ollama run qwen2.5-coder:7b`).

### 2️⃣ Pull & Run

Navigate to any folder containing your Terraform code, and run the following command to pull and start the agent:

```bash
docker run -p 8501:8501 -v ${PWD}:/app -e OPENAI_API_KEY="your_api_key_here" -e AWS_ACCESS_KEY_ID="your_aws_access_key" -e AWS_SECRET_ACCESS_KEY="your_aws_secret_key" -e AWS_DEFAULT_REGION="us-east-1" aditya040305/drift-guard-agent:latest
```

> **Note on Local LLMs (Ollama):** If you are using Ollama, set `-e LLM_BASE_URL="http://host.docker.internal:11434/v1"`, pass a dummy API key, and set `-e LLM_MODEL` to your local model name.

That's it! Open `http://localhost:8501` in your browser. The agent will automatically initialize Terraform and scan the code you mounted!

---

## 🛠️ Alternative: Running Locally (From Source)

If you prefer not to use Docker, you can run the agent locally on your machine:
1. Install **Python 3.8+**, **Terraform**, and the **AWS CLI**.
2. Clone the repository: `git clone https://github.com/Aditya-adhav/Drift-Guard-AI-Agent.git`
3. Navigate to the project: `cd Drift-Guard-AI-Agent`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `streamlit run src/app.py`

---

## 🎮 Using the App

1. The web interface will automatically open in your browser (`http://localhost:8501`).
2. In the **sidebar**, configure your LLM settings:
   - **LLM API Key**: Enter your OpenAI/Groq key (leave blank if using Ollama).
   - **LLM Base URL**: `https://api.openai.com/v1` (OpenAI) / `https://api.groq.com/openai/v1` (Groq) / `http://localhost:11434/v1` (Ollama).
   - **Model Name**: e.g., `gpt-4o`, `llama3-70b-8192`, or `qwen2.5-coder:7b`.
3. Click **Scan for Drift** to analyze your AWS environment.
4. If drift is detected, click **Trigger AI Remediation** to have the AI write the Terraform fix!

---

## 🧪 Testing Drift-Guard (Simulating Drift)

Want to see the AI agent in action? Here is a step-by-step guide to simulating a configuration drift manually:

1. **Provision Infrastructure First**: Navigate into the `example/` directory and ensure the sample `main.tf` has been applied to the cloud without any pending changes.
   ```bash
   terraform apply -auto-approve
   ```
2. **Create Manual Drift (The "Bad Actor")**: 
   - Log into your [AWS Management Console](https://console.aws.amazon.com/) (or use the AWS CLI).
   - Navigate to a resource defined in your `main.tf` (for example, a Security Group or an S3 Bucket).
   - Manually change a property! (e.g., Add a new Inbound Rule, change a description, or add a tag like `Environment = Manual`).
3. **Run the AI Agent**:
   - Go back to your terminal and start the app (`streamlit run src/app.py`).
   - Click **Scan for Drift**.
   - The application will detect the exact manual change you just made in the AWS Console.
4. **Trigger Remediation**: 
   - Click **Trigger AI Remediation**.
   - Watch the AI automatically write the Terraform HCL code required to incorporate your manual cloud change back into your local `main.tf` file!

---

<div align="center">

*Built with ❤️ for Agentic Cloud Security.*

**Made by Aditya Adhav**

</div>