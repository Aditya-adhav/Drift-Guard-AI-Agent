import streamlit as st
import time
import os
from detector import DriftDetector

# Page configuration
st.set_page_config(
    page_title="Drift-Guard | Agentic Cloud Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;600&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main .block-container {
        padding-top: 3rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }
    
    /* Headers & Typography */
    .hero-container {
        text-align: center;
        margin-bottom: 3.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        letter-spacing: -0.03em;
    }
    .hero-subtitle {
        font-size: 1.4rem;
        color: #94a3b8;
        font-weight: 300;
        margin-top: 0;
    }

    /* Cards & Glassmorphism */
    .metric-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 198, 255, 0.15);
        border: 1px solid rgba(0, 198, 255, 0.2);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .badge-security { background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.25)); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }
    .badge-cost { background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.25)); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
    .badge-neutral { background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.25)); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }

    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* App Background */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f8fafc;
    }

    /* Streamlit overrides for better UI */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(30, 41, 59, 0.5);
        min-height: 65px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Primary Button Glow */
    .stButton>button[data-baseweb="button"]:has(div>p) {
        /* Generic button fix if we want to target primary specifically, 
           Streamlit uses data-testid="baseButton-primary" */
    }
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
        color: #020617 !important;
    }
    [data-testid="baseButton-primary"]:hover {
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6) !important;
    }

    /* Code Text Area */
    .stTextArea textarea {
        font-family: 'Consolas', 'Courier New', monospace !important;
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(0, 198, 255, 0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 8px;
    }
    .stTextArea textarea:focus {
        border: 1px solid rgba(0, 198, 255, 0.8) !important;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class='hero-container'>
    <h1 class='hero-title'>Drift-Guard</h1>
    <p class='hero-subtitle'>Agentic Digital Twin for Infrastructure as Code</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("LLM API Key", type="password", help="Required for AI reasoning")
    base_url = st.text_input("LLM Base URL", value="http://localhost:11434/v1", help="Base URL for the OpenAI-compatible API")
    model_name = st.text_input("Model Name", value="qwen2.5-coder:7b", help="The name of the LLM model to use")
    tf_dir = st.text_input("Terraform Directory", value=".")
    
    st.markdown("---")
    st.markdown("### 🤖 Agent Settings")
    continuous_mode = st.toggle("Enable Continuous Monitoring", value=False, help="Automatically scans for drift every 60 seconds.")
    
    st.markdown("---")
    st.markdown("### 📝 System Prompt")
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.md")
    
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            default_prompt = f.read()
    else:
        default_prompt = "You are a helpful DevOps AI assistant."
        
    custom_prompt = st.text_area("Edit AI Instructions", value=default_prompt, height=300, help="Modify how the AI analyzes the plan and generates HCL.")
    
    if custom_prompt != default_prompt:
        with open(prompt_path, "w") as f:
            f.write(custom_prompt)
            
    st.markdown("---")
    st.markdown("### GitOps Status")
    
    # Init detector
    detector = DriftDetector(tf_dir=tf_dir, api_key=api_key if api_key else None, base_url=base_url, model_name=model_name)

# Initialize Session State
if 'step' not in st.session_state:
    st.session_state.step = "IDLE"
if 'plan_output' not in st.session_state:
    st.session_state.plan_output = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'plan_json' not in st.session_state:
    st.session_state.plan_json = None

# Helper functions for state transitions
def scan():
    if not api_key and not os.getenv("LLM_API_KEY") and not os.getenv("OPENAI_API_KEY") and not os.getenv("GROQ_API_KEY"):
        st.sidebar.error("LLM API Key is missing!")
        return False
        
    with st.spinner("Executing `terraform plan` to detect drift..."):
        exit_code, stdout = detector.run_terraform_plan()
        
        if exit_code == 0:
            st.session_state.step = "SYNCED"
        elif exit_code == 1:
            st.session_state.step = "ERROR"
            st.session_state.plan_output = stdout
        elif exit_code == 2:
            st.session_state.step = "DRIFT_DETECTED"
            st.session_state.plan_output = stdout
            st.session_state.plan_json = getattr(detector, 'plan_json', None)
            
    return True

def analyze():
    with st.spinner("AI Reasoning: Categorizing drift and generating HCL fix..."):
        detector.plan_json = st.session_state.get('plan_json')
        result = detector.analyze_and_remediate(st.session_state.plan_output)
        if result:
            if "error" in result:
                st.session_state.step = "AI_FAILED"
                st.session_state.error_msg = result["error"]
            else:
                st.session_state.analysis_result = result
                st.session_state.step = "REVIEW_FIX"
        else:
            st.session_state.step = "AI_FAILED"
            st.session_state.error_msg = "Maximum retries reached without generating valid HCL."

def apply_fix():
    with st.spinner("Applying corrected HCL to main.tf..."):
        hcl_code = st.session_state.get("edited_hcl", st.session_state.analysis_result.get("hcl_code"))
        detector.apply_fix(hcl_code)
        time.sleep(1) # Fake delay for effect
        st.session_state.step = "SYNCED"

def revert_infra():
    with st.spinner("Reverting cloud drift by enforcing local Terraform code..."):
        success, output = detector.revert_infra()
        if success:
            st.session_state.step = "SYNCED"
        else:
            st.session_state.step = "ERROR"
            st.session_state.plan_output = output

# --- Main Logic Flow ---

if st.session_state.step == "IDLE":
    st.info("System is ready. Initiate a scan to compare local code against the cloud state.")
    if st.button("🔍 Scan for Drift", use_container_width=True, type="primary"):
        if scan():
            st.rerun()
            
    if continuous_mode:
        st.markdown("### 🕒 Auto-Scan Active")
        progress_bar = st.progress(0, text="Next scan in 60 seconds...")
        for i in range(60):
            time.sleep(1)
            progress_bar.progress((i + 1) / 60, text=f"Next scan in {60 - (i+1)} seconds...")
        if scan():
            st.rerun()

elif st.session_state.step == "SYNCED":
    st.success("✅ System in Sync. No configuration drift detected.")
    if st.button("Rescan", use_container_width=True):
        st.session_state.step = "IDLE"
        st.rerun()
        
    if continuous_mode:
        st.markdown("### 🕒 Auto-Scan Active")
        progress_bar = st.progress(0, text="Next scan in 60 seconds...")
        for i in range(60):
            time.sleep(1)
            progress_bar.progress((i + 1) / 60, text=f"Next scan in {60 - (i+1)} seconds...")
        if scan():
            st.rerun()

elif st.session_state.step == "ERROR":
    st.error("Error executing terraform plan. Ensure you have run `terraform init` and your AWS credentials are set.")
    with st.expander("View Error Log", expanded=True):
        st.code(st.session_state.plan_output, language="text")
    if st.button("Retry", use_container_width=True):
        st.session_state.step = "IDLE"
        st.rerun()

elif st.session_state.step == "DRIFT_DETECTED":
    st.warning("⚠️ Configuration Drift Detected!")
    with st.expander("View Terraform Plan Diff", expanded=False):
        st.code(st.session_state.plan_output, language="hcl")
        
    st.markdown("### Agentic Remediation Required")
    st.info("Drift-Guard AI will now analyze the plan, categorize the risk, and generate a valid HCL code fix.")
    
    if st.button("🧠 Trigger AI Remediation", use_container_width=True, type="primary"):
        analyze()
        st.rerun()

elif st.session_state.step == "REVIEW_FIX":
    st.warning("⚠️ Configuration Drift Detected!")
    
    # Analysis UI layout
    cat = st.session_state.analysis_result.get("category", "Neutral")
    exp = st.session_state.analysis_result.get("explanation", "No explanation provided.")
    code = st.session_state.analysis_result.get("hcl_code", "")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### AI Categorization")
        
        badge_class = "badge-neutral"
        if cat == "Security Risk": badge_class = "badge-security"
        elif cat == "Cost Increase": badge_class = "badge-cost"
            
        st.markdown(f"<div class='metric-card'><h4>Category</h4><span class='badge {badge_class}'>{cat}</span><br><br><p><strong>Explanation:</strong> {exp}</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Human-in-the-Loop")
        st.info("Please review the proposed HCL code fix. Applying this fix will overwrite the local `main.tf` file to align it with the current cloud state.")
        
        # Action Buttons
        a_col, r_col, c_col = st.columns(3)
        with a_col:
            if st.button("📝 Update Local Code", help="Accept AI fix and update main.tf", use_container_width=True, type="primary"):
                apply_fix()
                st.rerun()
        with r_col:
            if st.button("🌩️ Revert Cloud Drift", help="Run terraform apply to wipe manual cloud changes", use_container_width=True):
                revert_infra()
                st.rerun()
        with c_col:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.step = "IDLE"
                st.rerun()

    with col2:
        st.markdown("### Proposed HCL Fix")
        st.text_area("You can manually edit the AI's proposed fix before applying:", value=code, height=400, key="edited_hcl")

elif st.session_state.step == "AI_FAILED":
    error_msg = st.session_state.get("error_msg", "AI Remediation failed to generate valid HCL after maximum retries.")
    st.error(f"AI Remediation failed: {error_msg}")
    if st.button("Retry Scan", use_container_width=True):
        st.session_state.step = "IDLE"
        st.rerun()

# Force streamlit reload