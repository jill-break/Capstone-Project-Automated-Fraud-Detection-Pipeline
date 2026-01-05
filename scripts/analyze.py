import sys
import csv

def analyze_fraud():
    # Read input from the pipe (stdin)
    input_data = sys.stdin.read().strip()
    
    if not input_data:
        print("No data received.")
        return

    # Parse the CSV data
    lines = input_data.split('\n')
    reader = csv.DictReader(lines)
    
    print("\n--- AI FRAUD ANALYSIS REPORT ---")
    
    for row in reader:
        user = row.get('user_id')
        amount = float(row.get('amount', 0))
        z_score = float(row.get('z_score', 0))
        category = row.get('merchant_category')

        # "AI" Logic: Generate Natural Language Explanation
        if z_score > 2:
            explanation = (
                f"CRITICAL ALERT: User {user} initiated a high-value transaction of ${amount:,.2f} "
                f"in the '{category}' category. \n"
                f"   -> Statistical Insight: The Z-Score is {z_score:.2f}, indicating this deviation "
                f"is significantly rare (top 2% of variance). Recommended Action: Immediate Freeze."
            )
            print(explanation)
        else:
            print(f"User {user}: Transaction appears normal.")

if __name__ == "__main__":
    analyze_fraud()