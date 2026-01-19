import sys
import os
import warnings
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
warnings.filterwarnings("ignore") # Hide warnings for the video
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def main():
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return

    # 1. Configure API
    try:
        genai.configure(api_key=api_key) # type: ignore
    except Exception as e:
        print(f"Error configuring API: {e}")
        return

    # 2. AUTO-SELECT MODEL (The Fix)
    # We ask the API for a list of models that support text generation
    # and pick the first one available to you.
    active_model_name = None
    try:
        for m in genai.list_models(): # type: ignore
            if 'generateContent' in m.supported_generation_methods:
                active_model_name = m.name
                break # Found one!
    except Exception as e:
        print(f"Error listing models: {e}")
        return

    if not active_model_name:
        print("No compatible Gemini models found for this API key.")
        return
    
    # 3. Read Piped Data
    try:
        if sys.stdin.isatty():
            print("No data received. Usage: cat anomalies.csv | python scripts/gemini_cli.py")
            return
        csv_data = sys.stdin.read().strip()
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    # 4. Construct Prompt
    prompt = f"""
    You are a Senior Fraud Analyst. 
    Analyze the following CSV transaction data:
    ```csv
    {csv_data}
    ```
    Task:
    1. Identify the transaction with a Z-Score greater than 2.
    2. State the recommended action for that transaction.
    3. Explain why this is an anomaly.
    4. Explain the recommended action.
    5. Format the output as a detailed report with sections and bullet points.
    """

    print(f"Sending data to Gemini (Model: {active_model_name})...")

    # 5. Call API
    try:
        model = genai.GenerativeModel(active_model_name) # type: ignore
        response = model.generate_content(prompt)
        
        print("\n" + "="*40)
        print("   GEMINI AI FRAUD ANALYSIS REPORT")
        print("="*40)
        print(response.text)
        print("\n" + "="*40)
        
        with open("fraud reports/fraud_report.md", "w") as f:
            f.write(response.text)
        print(f"Report saved to 'fraud reports/fraud_report.md'")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()