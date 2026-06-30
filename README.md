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

## 🚀 Getting Started

Follow these steps to set up the environment, install the necessary tools, and run Drift-Guard.

### 1️⃣ Install Prerequisites

<details>
<summary><b>A. Install Python</b></summary>

1. Download Python from the [official website](https://www.python.org/downloads/).
2. Run the installer and **check "Add Python to PATH"** at the bottom of the installation window.
3. Verify installation:
   ```bash
   python --version
   ```
</details>

<details>
<summary><b>B. Install Terraform</b></summary>

1. Download Terraform for your OS from [HashiCorp's website](https://developer.hashicorp.com/terraform/downloads).
2. Extract the executable and add its folder to your system's PATH.
3. Verify installation:
   ```bash
   terraform --version
   ```
</details>

<details>
<summary><b>C. Install AWS CLI & Authenticate</b></summary>

Since Drift-Guard uses Terraform to check AWS infrastructure, you need the AWS CLI installed.
1. Download the [AWS CLI Installer for Windows](https://awscli.amazonaws.com/AWSCLIV2.msi).
2. Run the installer.
3. Open a new terminal and log in using your AWS credentials:
   ```bash
   aws configure
   ```
4. Enter your `AWS Access Key ID`, `AWS Secret Access Key`, `Default region name` (e.g., `us-east-1`), and `Default output format` (e.g., `json`).
</details>

### 2️⃣ Set Up the LLM

Drift-Guard needs an AI model to reason about infrastructure drift. You have two main options:

> [!TIP]
> **Option A: Cloud Providers (OpenAI, Groq)**
> Get an API key from [OpenAI](https://platform.openai.com/) or [Groq](https://console.groq.com/). You will paste this key directly into the app UI later.

> [!TIP]
> **Option B: Local Open-Source Models (Ollama)**
> 1. Download and install [Ollama](https://ollama.com/).
> 2. Run a model locally in your terminal (e.g., Qwen 2.5 Coder):
>    ```bash
>    ollama run qwen2.5-coder:7b
>    ```
> 3. Leave Ollama running. The base URL for the app will be `http://localhost:11434/v1`.

### 3️⃣ Setup & Run

Navigate to the project folder and install the required Python libraries:

```bash
cd c:\Users\adity\OneDrive\Desktop\drift
pip install -r requirements.txt
```

Initialize Terraform to download the necessary providers (like AWS):

```bash
terraform init
```

Launch the beautiful Streamlit web interface:

```bash
streamlit run app.py
```

---

## 🐳 Running via Docker (Portable Tool)

You can run Drift-Guard as an isolated Docker container and scan any local Terraform project without installing Python or Terraform on your host machine!

1. **Build the Image:**
   ```bash
   docker build -t drift-guard-agent:latest .
   ```

2. **Run the Container (Mounting your code):**
   Navigate to the folder containing your Terraform code, and run:
   ```bash
   docker run -p 8501:8501 \
     -v ${PWD}:/app \
     -e OPENAI_API_KEY="your_api_key_here" \
     -e AWS_ACCESS_KEY_ID="your_aws_access_key" \
     -e AWS_SECRET_ACCESS_KEY="your_aws_secret_key" \
     -e AWS_DEFAULT_REGION="us-east-1" \
     drift-guard-agent:latest
   ```
   > **Note on Local LLMs (Ollama):** If you are using Ollama, set `-e LLM_BASE_URL="http://host.docker.internal:11434/v1"`, pass a dummy API key, and set `-e LLM_MODEL` to your local model name.

3. Open `http://localhost:8501` in your browser. The agent will automatically initialize Terraform and scan the code you mounted!

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

1. **Provision Infrastructure First**: Ensure your local `main.tf` has been applied to the cloud without any pending changes.
   ```bash
   terraform apply -auto-approve
   ```
2. **Create Manual Drift (The "Bad Actor")**: 
   - Log into your [AWS Management Console](https://console.aws.amazon.com/) (or use the AWS CLI).
   - Navigate to a resource defined in your `main.tf` (for example, a Security Group or an S3 Bucket).
   - Manually change a property! (e.g., Add a new Inbound Rule, change a description, or add a tag like `Environment = Manual`).
3. **Run the AI Agent**:
   - Go back to your terminal and start the app (`streamlit run app.py`).
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