import sys
import os
import argparse
import warnings
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
warnings.filterwarnings("ignore") 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def configure_gemini():
    """Configures the Gemini API."""
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
    except Exception as e:

        print(f"Error configuring API: {e}")
        sys.exit(1)

def get_active_model():
    """Returns the name of a reliable generative model."""
    # We prioritize 1.5-flash for speed and reliability in lab environments
    preferred_models = ['gemini-1.5-flash', 'gemini-1.5-pro']
    
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for model in preferred_models:
            for available in available_models:
                if model in available:
                    return available
        return available_models[0] if available_models else None
    except Exception as e:
        print(f"Error listing models: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Semantic Fraud Analyzer (CLI AI)")
    parser.add_argument("--scenario", required=True, help="Path to the fraud scenario description (txt)")
    parser.add_argument("--data", required=True, help="Path to the transaction data (csv)")
    args = parser.parse_args()

    # 1. Setup
    configure_gemini()
    model_name = get_active_model()
    if not model_name:
        print("No compatible Gemini models found.")
        sys.exit(1)
    
    # 2. Read Inputs
    try:
        with open(args.scenario, 'r', encoding='utf-8') as f:
            scenario_text = f.read()
        
        with open(args.data, 'r', encoding='utf-8') as f:
            csv_data = f.read()
    except Exception as e:
        print(f"Error reading input files: {e}")
        return

    # 3. Initialize Model with System Instructions
    # This separates the persona logic from the data, reducing 'malformed call' errors
    system_prompt = (
        "You are a Forensic Data Analyst. Your job is to perform SEMANTIC PROFILING on raw transaction data. "
        "You match qualitative behaviors described in scenarios to quantitative data in CSVs. "
        "Always cite specific transaction IDs or timestamps in your report."
    )

    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )

        # 4. Construct User Prompt
        user_prompt = f"""
        TASK:
        1. Analyze the Fraud Scenario below to understand the behavioral pattern.
        2. Identify the USER ID in the Raw Transaction Data that best fits this pattern.
        3. List the specific transactions that support your conclusion.
        4. Provide a 'Reasoning' section explaining the semantic match.

        --- FRAUD SCENARIO ---
        {scenario_text}

        --- RAW TRANSACTION DATA ---
        {csv_data}
        
        OUTPUT: Provide a professional Investigation Report in Markdown format.
        """

        print(f"Running Semantic Analysis with {model_name}...")
        
        # 5. Generate Content
        response = model.generate_content(user_prompt)
        
        # 6. Save and Display
        output_file = "semantic_fraud_report.md"
        with open(output_file, "w") as f:
            f.write(response.text)
            
        print("\n" + "="*40)
        print("   GEMINI SEMANTIC MATCH REPORT")
        print("="*40)
        print(response.text)
        print("\n" + "="*40)
        print(f"Report saved to '{output_file}'")
            
    except Exception as e:
        print(f"API Error: {e}")
        print("\nTIP: If you see 'malformed function call', try: pip install pydantic --upgrade")

if __name__ == "__main__":
    main()