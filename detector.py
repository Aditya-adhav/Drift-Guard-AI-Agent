import os
import subprocess
import json
from typing import Tuple, Optional, Dict
from openai import OpenAI

class DriftDetector:
    def __init__(self, tf_dir: str = ".", api_key: Optional[str] = None, base_url: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initializes the DriftDetector.
        
        :param tf_dir: Directory containing the Terraform configuration files.
        :param api_key: LLM API key. If not provided, looks for LLM_API_KEY, OPENAI_API_KEY, or GROQ_API_KEY.
        :param base_url: The base URL for the OpenAI-compatible API.
        :param model_name: The name of the model to use.
        """
        self.tf_dir = tf_dir
        self.api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY") or "dummy-local-key"
        self.base_url = base_url or os.getenv("LLM_BASE_URL") or "https://api.groq.com/openai/v1"
        self.model_name = model_name or os.getenv("LLM_MODEL") or "llama3-70b-8192"
        self.client = None
        
        # Load the system prompt from the local file
        prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.md")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are a helpful DevOps AI assistant."

    def run_terraform_plan(self) -> Tuple[int, str]:
        """
        Observe: Execute terraform plan and capture the stdout diff.
        Returns the exit code and stdout.
        -detailed-exitcode returns 0 (success/no diff), 1 (error), 2 (success/diff)
        """
        try:
            result = subprocess.run(
                ["terraform", "plan", "-detailed-exitcode", "-no-color", "-out=tfplan"],
                cwd=self.tf_dir,
                capture_output=True,
                text=True
            )
            exit_code = result.returncode
            stdout = result.stdout
            
            if exit_code == 2:
                json_res = subprocess.run(
                    ["terraform", "show", "-json", "tfplan"],
                    cwd=self.tf_dir,
                    capture_output=True,
                    text=True
                )
                self.plan_json = json_res.stdout
                
            return exit_code, stdout
        except Exception as e:
            return 1, str(e)
            
    def validate_hcl(self, hcl_code: str) -> Tuple[bool, str]:
        """
        Self-Correct: Writes temporary HCL code to main.tf and runs terraform validate.
        """
        main_tf_path = os.path.join(self.tf_dir, "main.tf")
        original_content = None
        
        if os.path.exists(main_tf_path):
            with open(main_tf_path, "r", encoding="utf-8") as f:
                original_content = f.read()
                
        try:
            with open(main_tf_path, "w", encoding="utf-8") as f:
                f.write(hcl_code)
                
            # Run without -json to get human readable errors which are better for LLMs
            result = subprocess.run(
                ["terraform", "validate", "-no-color"],
                cwd=self.tf_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True, "Valid HCL"
            else:
                # Terraform validate errors are usually printed to stdout or stderr
                error_output = result.stderr if result.stderr else result.stdout
                return False, error_output.strip()
        except Exception as e:
            return False, str(e)
        finally:
            if original_content is not None:
                with open(main_tf_path, "w", encoding="utf-8") as f:
                    f.write(original_content)
            elif os.path.exists(main_tf_path):
                os.remove(main_tf_path)

    def analyze_and_remediate(self, plan_output: str, max_retries: int = 3) -> Optional[Dict]:
        """
        Analyze & Reason & Act: Uses OpenAI to categorize drift and generate corrected HCL code.
        Returns a dictionary containing 'category', 'explanation', and 'hcl_code'.
        """
        import traceback
        with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
            logf.write("Starting analyze_and_remediate\n")
            
        if not self.client:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            
        # Read current main.tf content
        current_hcl = ""
        main_tf_path = os.path.join(self.tf_dir, "main.tf")
        if os.path.exists(main_tf_path):
            with open(main_tf_path, "r", encoding="utf-8") as f:
                current_hcl = f.read()

        # Extract Cloud JSON State
        cloud_state_context = ""
        try:
            with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                logf.write("--- JSON EXTRACTION DEBUG ---\n")
                if hasattr(self, 'plan_json') and self.plan_json:
                    logf.write("plan_json exists and is populated.\n")
                    plan_data = json.loads(self.plan_json)
                    rcs = plan_data.get('resource_changes', [])
                    logf.write(f"Found {len(rcs)} resource_changes.\n")
                    for rc in rcs:
                        change = rc.get('change', {})
                        logf.write(f"Processing rc: {rc.get('address')}, action: {change.get('actions')}\n")
                        before_state = change.get('before')
                        if before_state is not None:
                            logf.write(f"before_state is present! Type: {type(before_state)}\n")
                            res_addr = rc.get('address')
                            # Sanitize nulls and empty values to help AI
                            sanitized = {k: v for k, v in before_state.items() if v is not None and v != [] and v != {}}
                            cloud_state_context += f"\\nJSON representation of {res_addr} in the cloud:\\n```json\\n{json.dumps(sanitized, indent=2)}\\n```\\n"
                        else:
                            logf.write(f"before_state is missing or None.\n")
                else:
                    logf.write("plan_json does NOT exist or is empty!\n")
                logf.write("-----------------------------\n")
        except Exception as e:
            import traceback
            with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                logf.write(f"Exception extracting JSON state: {e}\n{traceback.format_exc()}\n")

        user_content = f"Here is the current main.tf code:\\n```hcl\\n{current_hcl}\\n```\\n\\nHere is the terraform plan output:\\n\\n{plan_output}\\n\\n{cloud_state_context}"
        
        with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
            logf.write(f"--- Prompt sent to AI ---\n{user_content}\n-----------------------\n")
            
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        for attempt in range(max_retries):
            try:
                with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                    logf.write(f"Attempt {attempt+1}\n")
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                
                ai_response = response.choices[0].message.content
                data = json.loads(ai_response)
                
                with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                    logf.write(f"AI Response parsed successfully\nRaw AI Output:\n{ai_response}\n\n")
                
                hcl_code = data.get("hcl_code", "")
                
                if isinstance(hcl_code, dict) or isinstance(hcl_code, list):
                    # AI accidentally put a JSON object/list instead of an HCL string
                    messages.append({"role": "assistant", "content": ai_response})
                    messages.append({
                        "role": "user",
                        "content": "You provided a JSON object for 'hcl_code'. The 'hcl_code' field MUST be a single String containing valid HashiCorp Configuration Language (HCL) syntax."
                    })
                    continue
                    
                if hcl_code is None:
                    hcl_code = ""
                hcl_code = hcl_code.strip()
                
                # Proactively strip markdown block if the model included it despite instructions
                if hcl_code.startswith("```hcl"):
                    hcl_code = hcl_code[6:]
                elif hcl_code.startswith("```"):
                    hcl_code = hcl_code[3:]
                if hcl_code.endswith("```"):
                    hcl_code = hcl_code[:-3]
                hcl_code = hcl_code.strip()
                
                data["hcl_code"] = hcl_code
                
                with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                    logf.write(f"Generated HCL Code:\n{hcl_code}\n\n")
                
                # Self-Correct: Validate HCL code
                is_valid, validation_output = self.validate_hcl(hcl_code)
                
                with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                    logf.write(f"Validation Result: {is_valid}, {validation_output}\n")
                
                if is_valid:
                    return data
                else:
                    # Append the failed attempt and the validation error to context
                    messages.append({"role": "assistant", "content": ai_response})
                    messages.append({
                        "role": "user", 
                        "content": f"The generated HCL code failed validation with the following error:\n{validation_output}\n\nPlease fix the syntax errors and provide ONLY the valid JSON response."
                    })
            except Exception as e:
                with open(os.path.join(self.tf_dir, "drift_guard_debug.log"), "a", encoding="utf-8") as logf:
                    logf.write(f"Exception: {str(e)}\n{traceback.format_exc()}\n")
                print(f"Attempt {attempt + 1} failed with error: {str(e)}")
                
                error_str = str(e)
                if "Connection error" in error_str or "Invalid API Key" in error_str or "invalid model ID" in error_str or "insufficient_quota" in error_str or "PermissionDeniedError" in traceback.format_exc() or "AuthenticationError" in traceback.format_exc() or "APIConnectionError" in traceback.format_exc() or "BadRequestError" in traceback.format_exc() or "NotFoundError" in traceback.format_exc() or "RateLimitError" in traceback.format_exc():
                    return {"error": f"LLM API Error: {error_str}"}

                messages.append({
                    "role": "user",
                    "content": f"An error occurred while parsing your response: {str(e)}. Please ensure you return valid JSON containing exactly the keys 'category', 'explanation', and 'hcl_code'."
                })
                
        return None

    def apply_fix(self, hcl_code: str, target_file: str = "main.tf"):
        """
        Apply: Overwrites local file with corrected HCL.
        """
        target_path = os.path.join(self.tf_dir, target_file)
        with open(target_path, "w") as f:
            f.write(hcl_code)

    def revert_infra(self) -> Tuple[bool, str]:
        """
        Revert Cloud Drift: Runs terraform apply -auto-approve to enforce local code on the cloud infrastructure.
        """
        try:
            result = subprocess.run(
                ["terraform", "apply", "-auto-approve", "-no-color"],
                cwd=self.tf_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr if result.stderr else result.stdout
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set in your environment
    agent = DriftDetector(tf_dir=".")
    exit_code, stdout = agent.run_terraform_plan()
    if exit_code == 2:
        result = agent.analyze_and_remediate(stdout)
        if result:
            print(f"Category: {result.get('category')}")
            print(f"Explanation: {result.get('explanation')}")
            print(result.get('hcl_code'))
            confirm = input("Confirm overwrite? (y/n): ")
            if confirm.lower() == 'y':
                agent.apply_fix(result.get('hcl_code'))
                print("Applied.")
